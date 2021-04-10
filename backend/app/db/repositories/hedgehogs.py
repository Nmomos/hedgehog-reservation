from typing import List

import app.db.repositories.queries.hedgehogs as query
from app.db.repositories.base import BaseRepository
from app.models.hedgehog import HedgehogCreate, HedgehogInDB, HedgehogUpdate
from app.models.user import UserInDB
from fastapi import HTTPException, status


class HedgehogsRepository(BaseRepository):
    async def create_hedgehog(
        self, *, new_hedgehog: HedgehogCreate, requesting_user: UserInDB
    ) -> HedgehogInDB:
        hedgehog = await self.db.fetch_one(
            query=query.CREATE_HEDGEHOG_QUERY,
            values={**new_hedgehog.dict(), "owner": requesting_user.id},
        )
        return HedgehogInDB(**hedgehog)

    async def get_hedgehog_by_id(
        self, *, id: int, requesting_user: UserInDB
    ) -> HedgehogInDB:
        hedgehog = await self.db.fetch_one(
            query=query.GET_HEDGEHOG_BY_ID_QUERY, values={"id": id}
        )
        if not hedgehog:
            return None
        return HedgehogInDB(**hedgehog)

    async def list_all_user_hedgehogs(
        self, requesting_user: UserInDB
    ) -> List[HedgehogInDB]:
        hedgehog_records = await self.db.fetch_all(
            query=query.LIST_ALL_USER_HEDGEHOGS_QUERY,
            values={"owner": requesting_user.id},
        )
        return [HedgehogInDB(**item) for item in hedgehog_records]

    async def update_hedgehog(
        self, *, hedgehog: HedgehogInDB, hedgehog_update: HedgehogUpdate
    ) -> HedgehogInDB:
        hedgehog_update_params = hedgehog.copy(
            update=hedgehog_update.dict(exclude_unset=True)
        )
        if hedgehog_update_params.color_type is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid hedgehog type. Cannot be None.",
            )
        updated_hedgehog = await self.db.fetch_one(
            query=query.UPDATE_HEDGEHOG_BY_ID_QUERY,
            values=hedgehog_update_params.dict(
                exclude={"owner", "created_at", "updated_at"}
            ),
        )
        return HedgehogInDB(**updated_hedgehog)

    async def delete_hedgehog_by_id(self, *, hedgehog: HedgehogInDB) -> int:
        return await self.db.execute(
            query=query.DELETE_HEDGEHOG_BY_ID_QUERY, values={"id": hedgehog.id}
        )
