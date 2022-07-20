from fastapi import (
    HTTPException,
    status
)


API_IS_DOWN = HTTPException(
    status_code=status.HTTP_424_FAILED_DEPENDENCY,
    detail="Currency converter API dependency is unavailable"
)

CURRENCY_NOT_SUPPORTED = lambda currency: HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=f"{currency} is not supported."
)