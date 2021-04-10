from typing import List

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.hedgehogs import (
    check_hedgehog_modification_permissions,
    get_hedgehog_by_id_from_path,
)
from app.db.repositories.hedgehogs import HedgehogsRepository
from app.models.hedgehog import (
    HedgehogCreate,
    HedgehogInDB,
    HedgehogPublic,
    HedgehogUpdate,
)
from app.models.user import UserInDB
from fastapi import APIRouter, Body, Depends, status

router = APIRouter()


@router.post(
    "/",
    response_model=HedgehogPublic,
    name="hedgehogs:create-hedgehog",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_hedgehog(
    new_hedgehog: HedgehogCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> HedgehogPublic:
    return await hedgehogs_repo.create_hedgehog(
        new_hedgehog=new_hedgehog, requesting_user=current_user
    )


@router.get(
    "/", response_model=List[HedgehogPublic], name="hedgehogs:list-all-user-hedgehogs"
)
async def list_all_user_hedgehogs(
    current_user: UserInDB = Depends(get_current_active_user),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> List[HedgehogPublic]:
    return await hedgehogs_repo.list_all_user_hedgehogs(requesting_user=current_user)


@router.get(
    "/{hedgehog_id}/",
    response_model=HedgehogPublic,
    name="hedgehogs:get-hedgehog-by-id",
)
async def get_hedgehog_by_id(
    hedgehog: HedgehogInDB = Depends(get_hedgehog_by_id_from_path),
) -> HedgehogPublic:
    return hedgehog


@router.put(
    "/{hedgehog_id}/",
    response_model=HedgehogPublic,
    name="hedgehogs:update-hedgehog-by-id",
    dependencies=[Depends(check_hedgehog_modification_permissions)],
)
async def update_hedgehog_by_id(
    hedgehog: HedgehogInDB = Depends(get_hedgehog_by_id_from_path),
    hedgehog_update: HedgehogUpdate = Body(..., embed=True),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> HedgehogPublic:
    return await hedgehogs_repo.update_hedgehog(
        hedgehog=hedgehog, hedgehog_update=hedgehog_update
    )


@router.delete(
    "/{hedgehog_id}/",
    response_model=int,
    name="hedgehogs:delete-hedgehog-by-id",
    dependencies=[Depends(check_hedgehog_modification_permissions)],
)
async def delete_hedgehog_by_id(
    hedgehog: HedgehogInDB = Depends(get_hedgehog_by_id_from_path),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> int:
    return await hedgehogs_repo.delete_hedgehog_by_id(hedgehog=hedgehog)
