from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.hedgehogs import HedgehogsRepository
from app.models.hedgehog import HedgehogCreate, HedgehogPublic, HedgehogUpdate
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

router = APIRouter()


@router.get('/',
            response_model=List[HedgehogPublic],
            name='hedgehogs:get-all-hedgehogs')
async def get_all_hedgehogs(
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository))
) -> List[HedgehogPublic]:
    return await hedgehogs_repo.get_all_hedgehogs()


@router.post('/',
             response_model=HedgehogPublic,
             name='hedgehogs:create-hedgehog',
             status_code=HTTP_201_CREATED)
async def create_new_hedgehog(
    new_hedgehog: HedgehogCreate = Body(..., embed=True),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> HedgehogPublic:
    created_hedgehog = await hedgehogs_repo.create_hedgehog(new_hedgehog=new_hedgehog)
    return created_hedgehog


@router.get('/{id}/', response_model=HedgehogPublic,
            name='hedgehogs:get-hedgehog-by-id')
async def get_hedgehog_by_id(
    id: int, hedgehogs_repo: HedgehogsRepository = Depends(
        get_repository(HedgehogsRepository
                       ))
) -> HedgehogPublic:
    hedgehog = await hedgehogs_repo.get_hedgehog_by_id(id=id)
    if not hedgehog:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='指定されたidのハリネズミは見つかりませんでした')
    return hedgehog


@router.put('/{id}/', response_model=HedgehogPublic,
            name='hedgehogs:update-hedgehog-by-id')
async def update_hedgehog_by_id(
    id: int = Path(..., ge=1, title='The ID of the hedgehog to update.'),
    hedgehog_update: HedgehogUpdate = Body(..., embed=True),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> HedgehogPublic:

    updated_hedgehog = await hedgehogs_repo.update_hedgehog(
        id=id,
        hedgehog_update=hedgehog_update)
    if not updated_hedgehog:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No hedgehog found with that id.')
    return updated_hedgehog


@router.delete('/{id}/', response_model=int, name='hedgehogs:delete-hedgehog-by-id')
async def delete_hedgehog_by_id(
    id: int = Path(..., ge=1, title='The ID of the hedgehog to delete.'),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository))
) -> int:
    deleted_id = await hedgehogs_repo.delete_hedgehog_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No hedgehog found with that id.')
    return deleted_id
