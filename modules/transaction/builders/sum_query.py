from sqlalchemy import select, func

from backend.modules.transaction.builders.base import TransactionBaseQueryBuilder
from backend.modules.transaction.models import Transaction


class TransactionValueSumQueryBuilder(TransactionBaseQueryBuilder):
    def _set_base_query(self):
        return select(func.sum(Transaction.value))  # pylint: disable=E1102
