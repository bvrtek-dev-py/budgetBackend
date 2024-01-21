from backend.src.core.modules.common.exceptions import ObjectDoesNotExist
from backend.src.core.modules.user.repository_interface import UserRepositoryInterface
from backend.src.core.modules.user.model import User


class UserRetrievalUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    async def get_by_id(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)

        if user is None:
            raise ObjectDoesNotExist()

        return user

    async def get_by_username_or_email(self, field: str) -> User:
        user = await self._repository.get_by_email(field)
        if user is not None:
            return user

        user = await self._repository.get_by_username(field)
        if user is not None:
            return user

        raise ObjectDoesNotExist()
