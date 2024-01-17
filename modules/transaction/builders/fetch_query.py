from sqlalchemy import select

from backend.modules.transaction.builders.base import TransactionBaseQueryBuilder
from backend.modules.transaction.models import Transaction


class TransactionFetchQueryBuilder(TransactionBaseQueryBuilder):
    def _set_base_query(self):
        return select(Transaction)
