from fastapi import APIRouter

from auth.api import router as auth
from converter.api import router as converter


router = APIRouter()
router.include_router(auth)
router.include_router(converter)
