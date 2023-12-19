from datetime import datetime
from typing import List, Any, Dict

from backend.modules.wallet.models import Wallet
from backend.tests.integration.user.data import get_user_db


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
            user=get_user_db()[0],
        ),
        Wallet(
            id=2,
            name="Konto_user_2",
            description="description",
            user_id=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user=get_user_db()[1],
        ),
    ]
