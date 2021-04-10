from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.db.repositories.hedgehogs import HedgehogsRepository
from app.models.hedgehog import HedgehogInDB
from app.models.user import UserInDB
from fastapi import Depends, HTTPException, Path, status


async def get_hedgehog_by_id_from_path(
    hedgehog_id: int = Path(..., ge=1),
    current_user: UserInDB = Depends(get_current_active_user),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> HedgehogInDB:
    hedgehog = await hedgehogs_repo.get_hedgehog_by_id(
        id=hedgehog_id, requesting_user=current_user
    )
    if not hedgehog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hedgehog found with that id.",
        )
    return hedgehog


def check_hedgehog_modification_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    hedgehog: HedgehogInDB = Depends(get_hedgehog_by_id_from_path),
) -> None:
    if hedgehog.owner != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action forbidden. Users are only able to modify hedgehogs they own",
        )
