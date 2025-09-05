from typing import Any, Dict, Optional, List
from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
import httpx
from time import time

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.asymmetric import rsa
from jose.utils import base64url_decode

from ..core.config import get_settings
from shared_schemas.security import TokenPayload, ROLE

_JWKS_CACHE: Dict[str, Any] = {}
_JWKS_TS: float = 0.0
_JWKS_TTL_SEC = 300

_ALLOWED_ROLES = {"admin", "observer", "participant"}


def _normalize_role(role: str) -> ROLE | None:
    value = (role or "").strip().lower()
    if value in ("admin", "observer", "participant"):
        return value

    if value in ("employee",):
        return "participant"

    if value in ("employee",):
        return "observer"

    return None


def _extract_roles_from_claims(claims: dict) -> list[ROLE]:
    roles: set[ROLE] = set()
    for role in (claims.get("realm_access", {}) or {}).get("roles", []) or []:
        norm_role = _normalize_role(role)
        if norm_role:
            roles.add(norm_role)
    single = _normalize_role(claims.get("role"))
    if single:
        roles.add(single)

    return sorted(roles)


def _has_role(payload: Dict[str, Any], role: str) -> bool:
    roles = payload.get("realm_access", {}).get("roles", []) or []
    norm = {_normalize_role(elem) for elem in roles}
    return _normalize_role(role) in norm


def _load_jwks() -> Dict[str, Any]:
    global _JWKS_CACHE, _JWKS_TS
    now = time()

    if _JWKS_CACHE and (now - _JWKS_TS) < _JWKS_TTL_SEC:
        return _JWKS_CACHE

    url = get_settings().keycloak_jwks_url
    try:
        resp = httpx.get(url, timeout=5.0)
        resp.raise_for_status()
        _JWKS_CACHE = resp.json()
        _JWKS_TS = now
        return _JWKS_CACHE

    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"JWKS fetch failed: {exc}")


def _pick_key(jwks: Dict[str, Any], kid: str) -> Optional[Dict[str, Any]]:
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key

    return None


def _public_key_from_jwk(jwk_dict: Dict[str, Any]):
    """
    Keycloak обычно отдаёт x5c. Берём его. Если нет — строим ключ из n/e.
    Возвращаем объект RSAPublicKey (cryptography), пригодный для jose.jwt.decode.
    """
    x5c = jwk_dict.get("x5c")
    if x5c and isinstance(x5c, list) and x5c:
        cert_pem = "-----BEGIN CERTIFICATE-----\n" + x5c[
            0] + "\n-----END CERTIFICATE-----\n"
        cert = load_pem_x509_certificate(cert_pem.encode("utf-8"))

        return cert.public_key()

    n_b = base64url_decode(jwk_dict["n"].encode("utf-8"))
    e_b = base64url_decode(jwk_dict["e"].encode("utf-8"))
    n = int.from_bytes(n_b, "big")
    e = int.from_bytes(e_b, "big")
    pub_numbers = rsa.RSAPublicNumbers(e, n)

    return pub_numbers.public_key()


def _map_role_from_keycloak(payload: Dict[str, Any]) -> str:
    roles: List[str] = payload.get("realm_access", {}).get("roles", []) or []
    normalized = {_normalize_role(elem) for elem in roles}
    for candidate in ("admin", "observer", "participant"):
        if candidate in normalized:
            return "participant" if candidate == "employee" else candidate

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No allowed role")


def _choose_effective_role(payload: Dict[str, Any], request_role: Optional[str]) -> str:
    """
    Если пришел X-Act-As и пользователь реально обладает этой ролью - используем её.
    Иначе - возвращаем default роль (_map_role_from_keycloak).
    """
    if request_role:
        req = _normalize_role(request_role)
        if req in _ALLOWED_ROLES and _has_role(payload, req):
            return "participant" if req == "employee" else req

    return _map_role_from_keycloak(payload)


def _to_token_payload(
        claims: dict,
        request_role: Optional[str]
) -> TokenPayload:
    all_roles = _extract_roles_from_claims(claims)
    effective: ROLE | None = None
    if request_role:
        req = _normalize_role(request_role)
        if req not in {"observer", "participant"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Act-As must be 'observer' or 'participant'"
            )

        if req not in all_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don`t have required role"
            )

        effective = req
    else:
        for role in ("admin", "observer", "participant"):
            if role in all_roles:
                effective = role
                break

    return TokenPayload(
        sub=claims.get("sub"),
        email=claims.get("email") or claims.get("preferred_username"),
        role=effective,
        roles=all_roles,
        exp=claims.get("exp"),
        iat=claims.get("iat"),
        iss=claims.get("iss"),
        aud=claims.get("aud"),
    )


def decode_token(token: str, request_role: Optional[str] = None) -> TokenPayload:
    settings = get_settings()
    if settings.auth_provider == "local":
        try:
            payload = jwt.decode(
                token,
                settings.auth_secret_key,
                algorithms=[settings.auth_algorithm],
                options={"verify_aud": False},
            )
            return _to_token_payload(payload, request_role)

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    try:
        headers = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Error decoding token headers.")

    kid = headers.get("kid")
    if not kid:
        raise HTTPException(status_code=401, detail="No kid in token header")

    jwks = _load_jwks()
    jwk_dict = _pick_key(jwks, kid)
    if not jwk_dict:
        raise HTTPException(status_code=401, detail="No matching JWK key")

    public_key = _public_key_from_jwk(jwk_dict)
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.keycloak_audience,
            issuer=settings.keycloak_issuer,
            options={"verify_at_hash": False},
        )
        return _to_token_payload(payload, request_role)

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}")
