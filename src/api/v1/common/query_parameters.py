from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, model_validator

from backend.src.api.v1.common.exceptions import DateRangeConflict


class DateRangeParameters(BaseModel):
    start_date: Optional[date] = Query(default=None)
    end_date: Optional[date] = Query(default=None)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "DateRangeParameters":
        if self.start_date is None or self.end_date is None:
            return self

        if self.start_date > self.end_date:
            raise DateRangeConflict()

        return self

    class ConfigDict:
        frozen = True
