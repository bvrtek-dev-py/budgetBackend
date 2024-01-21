from datetime import datetime, timedelta

from jose import jwt, JWTError

from backend.src.core.modules.auth.exceptions import InvalidCredentials
from backend.src.core.modules.auth.schemas import AuthenticatedUserDTO, CurrentUserDTO


class TokenService:
    def __init__(
        self,
        algorithm: str,
        refresh_token_secret_key: str,
        secret_key: str,
        token_expire_minutes: float,
    ):
        self.algorithm = algorithm
        self.refresh_token_secret_key = refresh_token_secret_key
        self.secret_key = secret_key
        self.token_expire_minutes = token_expire_minutes

    def create_access_token(self, data: AuthenticatedUserDTO) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode, key=self.secret_key, algorithm=self.algorithm
        )

    def create_refresh_token(self, data: AuthenticatedUserDTO) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode,
            key=self.refresh_token_secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> CurrentUserDTO:
        try:
            payload = jwt.decode(
                token=token, key=self.secret_key, algorithms=[self.algorithm]
            )
            email = payload.get("sub")
            user_id = payload.get("id")

            if email is None or user_id is None:
                raise InvalidCredentials()

            return CurrentUserDTO(id=user_id, email=email)
        except JWTError as exc:
            raise InvalidCredentials() from exc

    def get_expire_token_datetime(self) -> datetime:
        return datetime.now() + timedelta(minutes=self.token_expire_minutes)
