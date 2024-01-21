from passlib.context import CryptContext

from backend.src.core.modules.user.use_cases import UserRetrievalUseCase
from backend.src.core.modules.auth.exceptions import InvalidCredentials
from backend.src.core.modules.auth.schemas import ChangePasswordDTO
from backend.src.core.modules.user.interfaces import UserRepositoryInterface
from backend.src.core.modules.user.models import User


class PasswordHashService:
    def __init__(self, crypt: CryptContext):
        self._crypt = crypt

    def hash(self, password: str) -> str:
        return self._crypt.hash(password)  # type: ignore


class PasswordVerifyService:
    def __init__(self, crypt: CryptContext):
        self._crypt = crypt

    def verify(self, password: str, password_hash: str) -> bool:
        return self._crypt.verify(password, password_hash)  # type: ignore


class PasswordChangeService:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        retrieval_use_case: UserRetrievalUseCase,
        hash_service: PasswordHashService,
        verify_service: PasswordVerifyService,
    ):
        self._user_repository = user_repository
        self._retrieval_use_case = retrieval_use_case
        self._hash_service = hash_service
        self._verify_service = verify_service

    async def change_password(self, user_id: int, request: ChangePasswordDTO) -> User:
        user = await self._retrieval_use_case.get_by_id(user_id)

        if not self._verify_service.verify(request.current_password, user.password):
            raise InvalidCredentials()

        user.password = self._hash_service.hash(request.password)
        user = await self._user_repository.update(user)

        return user
