from backend.src.core.modules.user.interfaces import UserRepositoryInterface
from backend.src.core.modules.user.models import User
from backend.src.core.modules.common.exceptions import ObjectDoesNotExist


class UserRetrievalUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository

    async def get_by_id(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)

        if user is None:
            raise ObjectDoesNotExist()

        return user
