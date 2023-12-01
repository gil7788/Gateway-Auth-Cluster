from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
