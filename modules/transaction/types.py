from decimal import Decimal
from typing import Dict, Union

TotalType = Dict[str, Decimal]
MonthlyType = Dict[str, Dict[str, Decimal]]
StatisticsType = Dict[str, Union[TotalType, MonthlyType]]
