from sqlalchemy import select, func

from backend.src.core.modules.transaction.builders.base import (
    TransactionBaseQueryBuilder,
)
from backend.src.core.modules.transaction.model import Transaction


class TransactionValueSumQueryBuilder(TransactionBaseQueryBuilder):
    def _set_base_query(self):
        return select(func.sum(Transaction.value))  # pylint: disable=E1102
