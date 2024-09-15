from app.users.dao import UsersDAO
import pytest


@pytest.mark.parametrize("user_id,user_email,exists", [
    (1, "john.doe@example.com", True),
    (2, "jane.smith@example.com", True),
    (300, "...", False)
])
async def test_find_user_by_id(user_id, user_email, exists):
    user = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.email == user_email
        assert user.id == user_id
    else:
        assert not user

