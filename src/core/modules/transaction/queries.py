from datetime import datetime
from typing import Optional

from sqlalchemy import Select

from backend.src.core.modules.transaction.builders.sum_query import TransactionValueSumQueryBuilder
from backend.src.core.modules.transaction.enum import TransactionType


def build_sum_query_with_wallet_id(
    wallet_id: int,
    transaction_type: TransactionType,
    is_transfer: bool,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Select:
    return (
        TransactionValueSumQueryBuilder()
        .apply_transaction_type_filter(transaction_type)
        .apply_is_transfer_filter(is_transfer)
        .apply_wallet_id_filter(wallet_id)
        .apply_start_date_filter(start_date)
        .apply_end_date_filter(end_date)
        .build()
    )


def build_sum_query_with_user_id(
    user_id: int,
    transaction_type: TransactionType,
    is_transfer: bool,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Select:
    return (
        TransactionValueSumQueryBuilder()
        .apply_transaction_type_filter(transaction_type)
        .apply_is_transfer_filter(is_transfer)
        .apply_user_id_filter(user_id)
        .apply_start_date_filter(start_date)
        .apply_end_date_filter(end_date)
        .build()
    )
