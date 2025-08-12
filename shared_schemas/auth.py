from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordResetRequest(BaseModel):
    email: str
    base_url: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
