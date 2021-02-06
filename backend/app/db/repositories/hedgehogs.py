from typing import List

from app.db.repositories.base import BaseRepository
from app.models.hedgehog import HedgehogCreate, HedgehogInDB, HedgehogUpdate
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.hedgehogs as query

class HedgehogsRepository(BaseRepository):
    async def create_hedgehog(self, *, new_hedgehog: HedgehogCreate) -> HedgehogInDB:
        query_values = new_hedgehog.dict()
        hedgehog = await self.db.fetch_one(
            query=query.CREATE_HEDGEHOG_QUERY,
            values=query_values
        )
        return HedgehogInDB(**hedgehog)

    async def get_hedgehog_by_id(self, *, id: int) -> HedgehogInDB:
        hedgehog = await self.db.fetch_one(
            query=query.GET_HEDGEHOG_BY_ID_QUERY,
            values={'id': id}
        )
        if not hedgehog:
            return None
        return HedgehogInDB(**hedgehog)

    async def get_all_hedgehogs(self) -> List[HedgehogInDB]:
        hedgehog_records = await self.db.fetch_all(
            query=query.GET_ALL_HEDGEHOGS_QUERY)
        return [HedgehogInDB(**item) for item in hedgehog_records]

    async def update_hedgehog(
        self, *, id: int, hedgehog_update: HedgehogUpdate
    ) -> HedgehogInDB:
        hedgehog = await self.get_hedgehog_by_id(id=id)
        if not hedgehog:
            return None
        hedgehog_update_params = hedgehog.copy(
            update=hedgehog_update.dict(exclude_unset=True))
        if hedgehog_update_params.color_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid color type. Cannot be None.')

        try:
            updated_hedgehog = await self.db.fetch_one(
                query=query.UPDATE_HEDGEHOG_BY_ID_QUERY,
                values=hedgehog_update_params.dict()
            )
            return HedgehogInDB(**updated_hedgehog)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid update params.')

    async def delete_hedgehog_by_id(self, *, id: int) -> int:
        hedgehog = await self.get_hedgehog_by_id(id=id)
        if not hedgehog:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_HEDGEHOG_BY_ID_QUERY, values={'id': id})
        return deleted_id
