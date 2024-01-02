from datetime import date

from backend.api.v1.common.exceptions import DateRangeConflict


def validate_date_range(start_date: date, end_date: date) -> None:
    if start_date > end_date:
        raise DateRangeConflict
