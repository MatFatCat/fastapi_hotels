from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr
from app.users.dao import UsersDAO
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, **time_param) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(**time_param)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.JWT_ENCODING_ALG
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user
