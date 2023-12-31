from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.modules.auth.exceptions import InvalidCredentials
from backend.modules.auth.schemas import TokenData, CurrentUserData


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

    def create_access_token(self, data: TokenData) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode, key=self.secret_key, algorithm=self.algorithm
        )

    def create_refresh_token(self, data: TokenData) -> str:
        to_encode = data.model_copy().model_dump()
        to_encode.update({"exp": self.get_expire_token_datetime()})

        return jwt.encode(  # type: ignore
            claims=to_encode,
            key=self.refresh_token_secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> CurrentUserData:
        try:
            payload = jwt.decode(
                token=token, key=self.secret_key, algorithms=[self.algorithm]
            )
            email = payload.get("sub")
            user_id = payload.get("user_id")

            if email is None or user_id is None:
                raise InvalidCredentials()

            return CurrentUserData(id=user_id, email=email)
        except JWTError as exc:
            raise InvalidCredentials() from exc

    def get_expire_token_datetime(self) -> datetime:
        return datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
