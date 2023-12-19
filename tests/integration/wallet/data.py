from datetime import datetime
from typing import List

from backend.modules.wallet.models import Wallet
from backend.tests.integration.user.data import get_user_db


def get_wallet_data() -> List[Wallet]:
    return [
        Wallet(
            id=1,
            name="Konto",
            description="description",
            user_id=1,
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
