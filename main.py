import uvicorn
from fastapi import FastAPI

from backend.api.v1.auth.routers import router as auth_router
from backend.api.v1.category.routers import router as category_router
from backend.api.v1.subject.routers import router as subject_router
from backend.api.v1.transaction.routers import router as transaction_router
from backend.api.v1.user.routers.user import router as user_router
from backend.api.v1.user.routers.user_me import router as user_me_router
from backend.api.v1.wallet.routers import router as wallet_router
from backend.exception_handlers import http_exception_handler
from backend.modules.common.exceptions import BaseHttpException

app = FastAPI()

app.include_router(user_router)
app.include_router(user_me_router)
app.include_router(wallet_router)
app.include_router(category_router)
app.include_router(transaction_router)
app.include_router(subject_router)
app.include_router(auth_router)

app.add_exception_handler(BaseHttpException, http_exception_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
