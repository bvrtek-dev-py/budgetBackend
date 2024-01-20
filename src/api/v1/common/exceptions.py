from fastapi import HTTPException, status

DateRangeConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="End date must be greater than or equal to start date.",
)
