from datetime import date

from pydantic import BaseModel, model_validator

from backend.src.api.v1.common.exceptions import DateRangeConflict


class DateRangeParameters(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_passwords_match(self) -> "DateRangeParameters":
        date1 = self.start_date
        date2 = self.end_date

        if date1 is not None and date2 is not None and date1 >= date2:
            raise DateRangeConflict()

        return self

    class ConfigDict:
        frozen = True
