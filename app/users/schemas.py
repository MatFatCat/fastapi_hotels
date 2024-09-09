from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
