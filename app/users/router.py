from fastapi import APIRouter, Response, Depends
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users
from app.users.schemas import SUserRegister, SUserLogin, SUserProfile
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_token
from app.config import settings

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@auth_router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(name=user_data.name, email=user_data.email, hashed_password=hashed_password)


@auth_router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_token({"sub": str(user.id)}, minutes=settings.JWT_TOKEN_ACCESS_EXPIRE_M)
    token_refresh = create_token({"sub": str(user.id)}, days=settings.JWT_TOKEN_REFRESH_EXPIRE_D)
    await UsersDAO.update_refresh_token(user.id, token_refresh)
    response.set_cookie("booking_access_token", access_token, httponly=True)
    response.set_cookie("booking_refresh_token", token_refresh, httponly=True)

    return {"access_token": access_token, "token_refresh": token_refresh}


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    response.delete_cookie("booking_refresh_token")
    return {"Detail": "Successfully logged out from account!"}


@auth_router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)) -> SUserProfile:
    return SUserProfile(id=current_user.id, email=current_user.email, name=current_user.name)


# @auth_router.get("/all")
# async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
#     all_users = await UsersDAO.find_all()
#     return all_users
