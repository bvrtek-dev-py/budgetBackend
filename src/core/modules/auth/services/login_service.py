from backend.src.core.modules.auth.exceptions import InvalidCredentials
from backend.src.core.modules.auth.schemas import (
    SuccessAuthenticationDTO,
    AuthenticatedUserDTO,
)
from backend.src.core.modules.auth.services.password_services import (
    PasswordVerifyService,
)
from backend.src.core.modules.auth.services.token_service import TokenService
from backend.src.core.modules.user.use_cases import UserRetrievalUseCase


class LoginService:
    def __init__(
        self,
        verify_service: PasswordVerifyService,
        token_service: TokenService,
        user_retrieval_use_case: UserRetrievalUseCase,
    ):
        self._verify_service = verify_service
        self._token_service = token_service
        self._user_retrieval_use_case = user_retrieval_use_case

    async def login(self, username: str, password: str):
        user = await self._authenticate(username, password)

        return SuccessAuthenticationDTO(
            token_type="Bearer",
            access_token=self._token_service.create_access_token(user),
            refresh_token=self._token_service.create_refresh_token(user),
            expired_at=self._token_service.get_expire_token_datetime(),
        )

    async def _authenticate(self, username: str, password: str) -> AuthenticatedUserDTO:
        user = await self._user_retrieval_use_case.get_by_username_or_email(username)

        if not self._verify_service.verify(password, user.password):
            raise InvalidCredentials()

        return AuthenticatedUserDTO(id=user.id, sub=user.email)
