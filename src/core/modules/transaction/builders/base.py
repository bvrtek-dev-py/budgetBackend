from datetime import date
from typing import Optional

from sqlalchemy import Select, ColumnElement

from backend.src.core.modules.transaction.enums import TransactionType
from backend.src.core.modules.transaction.models import Transaction


class TransactionBaseQueryBuilder:
    def __init__(self):
        self.query: Select = self._set_base_query()

    def _apply_filter(
        self, filter_condition: ColumnElement[bool]
    ) -> "TransactionBaseQueryBuilder":
        self.query = self.query.where(filter_condition)

        return self

    def apply_name(self, name: str) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.name == name)

        return self

    def apply_date(self, date_value: date) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.date == date_value)

        return self

    def apply_wallet_id_filter(self, wallet_id: int) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.wallet_id == wallet_id)

        return self

    def apply_user_id_filter(self, user_id: int) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.user_id == user_id)

        return self

    def apply_subject_id_filter(self, subject_id: int) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.subject_id == subject_id)

        return self

    def apply_category_id_filter(
        self, category_id: int
    ) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.category_id == category_id)

        return self

    def apply_is_transfer_filter(
        self, is_transfer: bool
    ) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.is_transfer == is_transfer)

        return self

    def apply_transaction_type_filter(
        self, transaction_type: TransactionType
    ) -> "TransactionBaseQueryBuilder":
        self._apply_filter(Transaction.type == transaction_type)

        return self

    def apply_start_date_filter(
        self, start_date: Optional[date]
    ) -> "TransactionBaseQueryBuilder":
        if start_date is not None:
            self._apply_filter(Transaction.date >= start_date)

        return self

    def apply_end_date_filter(
        self, end_date: Optional[date]
    ) -> "TransactionBaseQueryBuilder":
        if end_date is not None:
            self._apply_filter(Transaction.date <= end_date)

        return self

    def _set_base_query(self) -> Select:
        raise NotImplementedError()

    def build(self) -> Select:
        return self.query
