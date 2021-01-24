from app.db.repositories.base import BaseRepository
from app.models.hedgehog import HedgehogCreate, HedgehogInDB

CREATE_HEDGEHOG_QUERY = """
    INSERT INTO hedgehogs (name, description, age, color_type)
    VALUES (:name, :description, :age, :color_type)
    RETURNING id, name, description, age, color_type;
"""


class HedgehogsRepository(BaseRepository):
    async def create_hedgehog(self, *, new_hedgehog: HedgehogCreate) -> HedgehogInDB:
        query_values = new_hedgehog.dict()
        hedgehog = await self.db.fetch_one(query=CREATE_HEDGEHOG_QUERY, values=query_values)

        return HedgehogInDB(**hedgehog)
