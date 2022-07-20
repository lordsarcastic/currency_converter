from fastapi import HTTPException, status


APIIsDown = HTTPException(
    status_code=status.HTTP_424_FAILED_DEPENDENCY,
    detail="Currency converter API dependency is unavailable",
)

CurrencyNotSupported = lambda currency: HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=f"{currency} is not supported."
)
