from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Select

from backend.modules.transaction.models import Transaction


def filter_query_by_date_range(
    query: Select,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Select:
    if start_date is not None:
        query = query.where(Transaction.date >= start_date)

    if end_date is not None:
        query = query.where(Transaction.date <= end_date)

    return query
