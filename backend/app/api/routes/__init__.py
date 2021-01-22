from fastapi import APIRouter
from app.api.routes.hedgehogs import router as hedgehogs_router


router = APIRouter()
router.include_router(hedgehogs_router, prefix="/hedgehogs", tags=["hedgehogs"])
