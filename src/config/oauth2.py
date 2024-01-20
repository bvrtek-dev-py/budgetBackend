from fastapi.security import OAuth2PasswordBearer

from backend.src.config.auth import LOGIN_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=LOGIN_URL)
