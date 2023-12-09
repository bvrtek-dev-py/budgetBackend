from dotenv import load_dotenv
import os

load_dotenv()

DB_ROOT_PASSWORD: str = os.getenv("DB_ROOT_PASSWORD")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: int = int(os.getenv("DB_PORT"))
DB_NAME: str = os.getenv("DB_NAME")

DATABASE_URL: str = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
