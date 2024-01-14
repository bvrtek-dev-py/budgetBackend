import functools
from datetime import datetime, date
from decimal import Decimal
from typing import List, Dict, Any

from backend.modules.auth.dependencies import (
    _get_crypt_context,
)
from backend.modules.auth.services import PasswordHashService
from backend.modules.category.models import Category
from backend.modules.subject.models import Subject
from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.models import Transaction
from backend.modules.user.models import User
from backend.modules.wallet.models import Wallet

BASE_USER_ID: int = 1
BASE_USER_DATA: Dict[str, str] = {
    "first_name": "name",
    "last_name": "last",
    "username": "username",
    "email": "email@email.pl",
}


@functools.cache
def hash_password(password: str) -> str:
    hash_service = PasswordHashService(_get_crypt_context())
    return hash_service.hash(password)


def get_user_db() -> List[User]:
    return [
        User(
            id=BASE_USER_ID,
            first_name=BASE_USER_DATA["first_name"],
            last_name=BASE_USER_DATA["last_name"],
            username=BASE_USER_DATA["username"],
            email=BASE_USER_DATA["email"],
            password=hash_password("1234"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            wallets=[get_wallet_data()[0]],
            subjects=[get_subject_data()[0]],
            transactions=[get_transaction_data()[0], get_transaction_data()[1]],
        ),
        User(
            id=2,
            first_name="Łukasz",
            last_name="Borys",
            username="user",
            email="user@email.pl",
            password=hash_password("1234"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            wallets=[get_wallet_data()[1]],
            subjects=[get_subject_data()[1]],
        ),
    ]


BASE_WALLET_ID: int = 1
BASE_WALLET_DATA: Dict[str, Any] = {
    "name": "Konto",
    "description": "description",
    "user_id": 1,
}


def get_wallet_data() -> List[Wallet]:
    return [
        Wallet(
            id=BASE_WALLET_ID,
            name=BASE_WALLET_DATA["name"],
            description=BASE_WALLET_DATA["description"],
            user_id=BASE_WALLET_DATA["user_id"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            transactions=[get_transaction_data()[0], get_transaction_data()[1]],
        ),
        Wallet(
            id=2,
            name="Konto_user_2",
            description="description",
            user_id=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            transactions=[get_transaction_data()[2]],
        ),
    ]


BASE_SUBJECT_ID = 1
BASE_SUBJECT_DATA = {
    "id": BASE_SUBJECT_ID,
    "name": "Subject 1",
}


def get_subject_data() -> List[Subject]:
    return [
        Subject(
            **BASE_SUBJECT_DATA,
            user_id=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        Subject(
            id=2,
            name="Subject 2",
            user_id=2,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        Subject(
            id=3,
            name="Subject 3",
            user_id=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
    ]


BASE_CATEGORY_ID: int = 1
BASE_CATEGORY_DATA = {
    "id": BASE_CATEGORY_ID,
    "name": "Base",
    "user_id": 1,
    "transaction_type": TransactionType.EXPENSE,
}


def get_category_data() -> List[Category]:
    return [
        Category(
            **BASE_CATEGORY_DATA,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Category(
            id=2,
            name="Category 2",
            user_id=2,
            transaction_type=TransactionType.INCOME,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Category(
            id=3,
            name="Category 3",
            user_id=1,
            transaction_type=TransactionType.INCOME,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


BASE_TRANSACTION_ID = 1
BASE_TRANSACTION_DATA = {
    "id": BASE_TRANSACTION_ID,
    "name": "name",
    "description": "description",
    "date": date.today(),
    "type": TransactionType.INCOME,
    "value": Decimal("20.00"),
}
BASE_TRANSACTION_RESPONSE = BASE_TRANSACTION_DATA | {
    "date": date.today().strftime("%Y-%m-%d"),
    "value": str(Decimal("20.00")),
}


def get_transaction_data() -> List[Transaction]:
    return [
        Transaction(
            **BASE_TRANSACTION_DATA,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=BASE_USER_ID,
            wallet_id=BASE_WALLET_ID,
            subject_id=BASE_SUBJECT_ID,
            category_id=BASE_CATEGORY_ID,
        ),
        Transaction(
            **(BASE_TRANSACTION_DATA | {"id": 2, "type": TransactionType.EXPENSE}),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=BASE_USER_ID,
            wallet_id=BASE_WALLET_ID,
            subject_id=BASE_SUBJECT_ID,
            category_id=BASE_CATEGORY_ID,
        ),
        Transaction(
            id=3,
            name="name",
            value=Decimal("20.00"),
            description="description",
            date=date.today(),
            type=TransactionType.INCOME,
            user_id=2,
            wallet_id=2,
            subject_id=2,
            category_id=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
