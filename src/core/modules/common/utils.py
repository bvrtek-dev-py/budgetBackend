from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_first_day_of_month(date: datetime) -> datetime:
    return date.replace(day=1)


def get_last_day_of_month(date: datetime) -> datetime:
    return date + relativedelta(months=1, days=-1)
