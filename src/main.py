import uvicorn
from fastapi import FastAPI

from backend.src.api.v1.auth.routers import router as auth_router
from backend.src.api.v1.category.routers import router as category_router
from backend.src.api.v1.subject.routers.subject import router as subject_router
from backend.src.api.v1.subject.routers.subject_transactions import (
    router as subject_transactions_router,
)
from backend.src.api.v1.transaction.routers import router as transaction_router
from backend.src.api.v1.user.routers.user import router as user_router
from backend.src.api.v1.user.routers.user_me import router as user_me_router
from backend.src.api.v1.user.routers.user_me_transactions import (
    router as user_me_transactions_router,
)
from backend.src.api.v1.wallet.routers.wallet import router as wallet_router
from backend.src.api.v1.wallet.routers.wallet_transactions import (
    router as wallet_transactions_router,
)
from backend.src.api.v1.wallet.routers.wallet_transfer import router as wallet_transfer
from backend.src.exception_handlers import http_exception_handler
from backend.src.core.modules.common.exceptions import BaseHttpException

app = FastAPI()

app.include_router(user_router)
app.include_router(user_me_router)
app.include_router(user_me_transactions_router)
app.include_router(wallet_router)
app.include_router(wallet_transactions_router)
app.include_router(wallet_transfer)
app.include_router(category_router)
app.include_router(transaction_router)
app.include_router(subject_router)
app.include_router(subject_transactions_router)
app.include_router(auth_router)

app.add_exception_handler(BaseHttpException, http_exception_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
