from sqlalchemy import select

from backend.src.core.modules.transaction.builders.base import (
    TransactionBaseQueryBuilder,
)
from backend.src.core.modules.transaction.models import Transaction


class TransactionFetchQueryBuilder(TransactionBaseQueryBuilder):
    def _set_base_query(self):
        return select(Transaction)
