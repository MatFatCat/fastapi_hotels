from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.users.auth import authenticate_user, create_token
from typing import Optional, Union
from app.users.dependencies import get_current_user
from app.logging.logger import logger
from app.users.models import Users
from fastapi import Depends


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)

        if user:
            access_token = create_token({"sub": str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request, user: Users = Depends(get_current_user)) -> Union[RedirectResponse, bool]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return True


authentication_backend = AdminAuth(secret_key="...")
