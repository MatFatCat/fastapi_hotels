from fastapi import Request, Depends, Response
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import TokenExpiredException, NoTokenException, IncorrectTokenFormatException,\
    UserIsNotPresentException
from app.users.auth import create_token
from app.config import settings
from app.logging.logger import logger


def get_token(request: Request):
    jwt_token = request.cookies.get("booking_access_token")
    if not jwt_token:
        raise NoTokenException
    return jwt_token


async def get_current_user(request: Request, response: Response, jwt_token: str = Depends(get_token)) -> Users:
    try:
        payload = jwt.decode(
            jwt_token, settings.JWT_SECRET_KEY, settings.JWT_ENCODING_ALG
        )
    except JWTError:
        token_refresh = request.cookies.get("booking_refresh_token")
        if not token_refresh:
            raise IncorrectTokenFormatException
        try:
            payload = jwt.decode(token_refresh, settings.JWT_SECRET_KEY, settings.JWT_ENCODING_ALG)
            user_id: str = payload.get("sub")
            if not user_id:
                raise UserIsNotPresentException

            user = await UsersDAO.find_by_id(int(user_id))
            if not user or user.token_refresh != token_refresh:
                raise TokenExpiredException

            new_access_token = create_token({"sub": str(user.id)}, minutes=settings.JWT_TOKEN_ACCESS_EXPIRE_M)

            response.set_cookie("booking_access_token", new_access_token, httponly=True, secure=True)
            payload = jwt.decode(new_access_token, settings.JWT_SECRET_KEY, settings.JWT_ENCODING_ALG)
        except JWTError:
            raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)): #  делаем еще одну зависимость и
                                                                                   # зависим от нее в том эндпойнте,
                                                                                   # которые доступны только, условно,
                                                                                   # админам, или любмы другим ролям
    # if current_user.role != "admin": # по факту работает как middleware, проверяем роль на этапе запроса
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return current_user
