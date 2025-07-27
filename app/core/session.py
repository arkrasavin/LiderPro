from fastapi import Request, Response
from itsdangerous import URLSafeSerializer

SECRET_KEY = "super-secret"
serializer = URLSafeSerializer(SECRET_KEY)

def create_session_token(login: str, role: str):
    return serializer.dumps({"login": login, "role": role})

def read_session_token(token: str):
    try:
        return serializer.loads(token)
    except Exception:
        return None

def set_session_cookie(response: Response, login: str, role: str):
    token = create_session_token(login, role)
    response.set_cookie(key="session", value=token, httponly=True)

def get_current_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        return None
    return read_session_token(token)