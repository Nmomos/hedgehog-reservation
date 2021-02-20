from app.api.routes.hedgehogs import router as hedgehogs_router
from app.api.routes.users import router as users_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(hedgehogs_router, prefix="/hedgehogs", tags=["hedgehogs"])
router.include_router(users_router, prefix="/users", tags=["users"])
