import functools
from datetime import datetime
from typing import List

from backend.modules.auth.dependencies import (
    _get_crypt_context,
)
from backend.modules.auth.services import PasswordHashService
from backend.modules.user.models import User


base_user_data = {
    "first_name": "name",
    "last_name": "last",
    "username": "username",
    "email": "email@email.pl",
}


@functools.cache
def hash_password(password: str) -> str:
    hash_service = PasswordHashService(_get_crypt_context())
    return hash_service.hash(password)


def get_user_db() -> List[User]:
    return [
        User(
            id=1,
            first_name=base_user_data["first_name"],
            last_name=base_user_data["last_name"],
            username=base_user_data["username"],
            email=base_user_data["email"],
            password=hash_password("1234"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        User(
            id=2,
            first_name="Łukasz",
            last_name="Borys",
            username="user",
            email="user@email.pl",
            password=hash_password("1234"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
