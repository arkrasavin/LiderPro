#!/usr/bin/env python3
from pathlib import Path
import os
import sys
import yaml
from collections import OrderedDict
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "services"
SHARED = ROOT / "shared_openapi" / "components.yaml"
OUTDIR = ROOT / "gateway"
OUTFILE = OUTDIR / "openapi.yaml"

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def merge_paths(acc_paths: dict, new_paths: dict, src_name: str):
    for p, ops in (new_paths or {}).items():
        if p not in acc_paths:
            acc_paths[p] = ops
            continue
        for method, op in (ops or {}).items():
            if method not in acc_paths[p]:
                acc_paths[p][method] = op
            else:
                # оставляем первую версию; просто предупреждаем
                old_op = acc_paths[p][method]
                if old_op.get("operationId") != op.get("operationId"):
                    print(f"[WARN] Path-method conflict: {p} {method} from {src_name}. Keeping first.", file=sys.stderr)

def merge_tags(acc_tags: list, new_tags: list):
    acc_by_name = {t.get("name"): t for t in acc_tags}
    for t in (new_tags or []):
        name = t.get("name")
        if name and name not in acc_by_name:
            acc_by_name[name] = t
    return list(acc_by_name.values())

def to_plain(obj):
    """Рекурсивно переводит OrderedDict -> dict, списки внутри тоже чистит."""
    if isinstance(obj, OrderedDict):
        return {k: to_plain(v) for k, v in obj.items()}
    if isinstance(obj, dict):
        return {k: to_plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_plain(i) for i in obj]
    return obj

def main():
    if not SHARED.exists():
        print(f"[ERR] Missing shared components: {SHARED}", file=sys.stderr)
        sys.exit(1)

    gateway_url = os.environ.get("GATEWAY_URL", "http://localhost:8080")

    service_files = sorted(SERVICES.glob("*/docs/openapi.yaml"))
    if not service_files:
        print(f"[ERR] No service specs found under {SERVICES}/**/docs/openapi.yaml", file=sys.stderr)
        sys.exit(1)

    shared = load_yaml(SHARED)
    shared_components = deepcopy((shared or {}).get("components", {}))

    # Подстановка публичного OIDC-issuer при сборке (опционально)
    issuer = os.environ.get("KEYCLOAK_PUBLIC_ISSUER")
    if issuer:
        try:
            openid = shared_components.get("securitySchemes", {}).get("OpenID", {})
            url = openid.get("openIdConnectUrl")
            if url and "${KEYCLOAK_ISSUER}" in url:
                openid["openIdConnectUrl"] = url.replace("${KEYCLOAK_ISSUER}", issuer)
        except Exception as e:
            print(f"[WARN] OIDC substitution failed: {e}", file=sys.stderr)

    merged = OrderedDict()
    merged["openapi"] = "3.0.3"
    merged["info"] = {
        "title": "LiderPro — API Gateway",
        "version": "1.0.0",
        "description": "Сводная спецификация всех микросервисов LiderPro."
    }
    merged["servers"] = [{"url": gateway_url}]
    merged["security"] = [{"OpenID": []}]

    all_paths = OrderedDict()
    all_tags = []

    for f in service_files:
        doc = load_yaml(f)
        merge_paths(all_paths, doc.get("paths", {}), src_name=str(f.parent.parent.name))
        all_tags = merge_tags(all_tags, doc.get("tags", []))

    merged["paths"] = all_paths
    merged["tags"] = all_tags
    merged["components"] = shared_components

    OUTDIR.mkdir(parents=True, exist_ok=True)
    with OUTFILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(to_plain(merged), f, allow_unicode=True, sort_keys=False)

    print(f"[OK] Wrote {OUTFILE}")

if __name__ == "__main__":
    main()
