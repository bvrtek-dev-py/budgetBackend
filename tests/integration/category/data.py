from datetime import datetime
from typing import List

from backend.modules.category.models import Category
from backend.modules.transaction.enums import TransactionType
from backend.tests.integration.user.data import get_user_db

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
            user=get_user_db()[0]
        ),
        Category(
            id=2,
            name="Category 2",
            user_id=2,
            transaction_type=TransactionType.INCOME,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user=get_user_db()[1],
        ),
        Category(
            id=3,
            name="Category 3",
            user_id=1,
            transaction_type=TransactionType.INCOME,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user=get_user_db()[0],
        ),
    ]
