from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.user import UserCreate, UserPublic
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED


router = APIRouter()
@router.post("/",
             response_model=UserPublic,
             name="users:register-new-user",
             status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)
    return created_user
