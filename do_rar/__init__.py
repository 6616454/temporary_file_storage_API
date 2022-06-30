from .api import router as do_rar_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(do_rar_router)
