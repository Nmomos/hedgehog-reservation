from typing import Dict, List, Optional, Union

import pytest
from app.db.repositories.hedgehogs import HedgehogsRepository
from app.models.hedgehog import HedgehogCreate, HedgehogInDB, HedgehogPublic
from app.models.user import UserInDB
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_hedgehog():
    return HedgehogCreate(
        name="test hedgehog",
        description="test description",
        age=0.0,
        color_type="SOLT & PEPPER",
    )


@pytest.fixture
async def test_hedgehogs_list(db: Database, test_user2: UserInDB) -> List[HedgehogInDB]:
    hedgehog_repo = HedgehogsRepository(db)
    return [
        await hedgehog_repo.create_hedgehog(
            new_hedgehog=HedgehogCreate(
                name="test hedgehog {i}",
                description="test description",
                age=0.0,
                color_type="SOLT & PEPPER",
            ),
            requesting_user=test_user2,
        )
        for i in range(5)
    ]


class TestHedgehogsRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("hedgehogs:create-hedgehog"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestCreateHedgehog:
    async def test_valid_input_creates_hedgehog_belonging_to_user(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        new_hedgehog: HedgehogCreate,
    ) -> None:
        res = await authorized_client.post(
            app.url_path_for("hedgehogs:create-hedgehog"),
            json={"new_hedgehog": new_hedgehog.dict()},
        )
        assert res.status_code == status.HTTP_201_CREATED
        created_hedgehog = HedgehogPublic(**res.json())
        assert created_hedgehog.name == new_hedgehog.name
        assert created_hedgehog.age == new_hedgehog.age
        assert created_hedgehog.description == new_hedgehog.description
        assert created_hedgehog.color_type == new_hedgehog.color_type
        assert created_hedgehog.owner == test_user.id

    async def test_unauthorized_user_unable_to_create_hedgehog(
        self, app: FastAPI, client: AsyncClient, new_hedgehog: HedgehogCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("hedgehogs:create-hedgehog"),
            json={"new_hedgehog": new_hedgehog.dict()},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"name": "test_name"}, 422),
            ({"age": 2}, 422),
            ({"name": "test_name", "description": "test"}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        invalid_payload: Dict[str, Union[str, float]],
        test_hedgehog: HedgehogCreate,
        status_code: int,
    ) -> None:
        res = await authorized_client.post(
            app.url_path_for("hedgehogs:create-hedgehog"),
            json={"new_hedgehog": invalid_payload},
        )
        assert res.status_code == status_code


class TestGetHedgehog:
    async def test_get_hedgehog_by_id(
        self, app: FastAPI, authorized_client: AsyncClient, test_hedgehog: HedgehogInDB
    ) -> None:
        res = await authorized_client.get(
            app.url_path_for(
                "hedgehogs:get-hedgehog-by-id", hedgehog_id=test_hedgehog.id
            )
        )
        assert res.status_code == status.HTTP_200_OK
        hedgehog = HedgehogInDB(**res.json())
        assert hedgehog == test_hedgehog

    async def test_unauthorized_users_cant_access_hedgehogs(
        self, app: FastAPI, client: AsyncClient, test_hedgehog: HedgehogInDB
    ) -> None:
        res = await client.get(
            app.url_path_for(
                "hedgehogs:get-hedgehog-by-id", hedgehog_id=test_hedgehog.id
            )
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "id, status_code",
        ((50000, 404), (-1, 422), (None, 422)),
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, authorized_client: AsyncClient, id: int, status_code: int
    ) -> None:
        res = await authorized_client.get(
            app.url_path_for("hedgehogs:get-hedgehog-by-id", hedgehog_id=id)
        )
        assert res.status_code == status_code

    async def test_get_all_hedgehogs_returns_only_user_owned_hedgehogs(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        db: Database,
        test_hedgehog: HedgehogInDB,
        test_hedgehogs_list: List[HedgehogInDB],
    ) -> None:
        res = await authorized_client.get(
            app.url_path_for("hedgehogs:list-all-user-hedgehogs")
        )
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        hedgehogs = [HedgehogInDB(**item) for item in res.json()]
        assert test_hedgehog in hedgehogs
        for hedgehog in hedgehogs:
            assert hedgehog.owner == test_user.id
        assert all(c not in hedgehogs for c in test_hedgehogs_list)


class TestUpdateHedgehog:
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        (
            (["name"], ["new fake hedgehog name"]),
            (["description"], ["new fake hedgehog description"]),
            (["age"], [3.14]),
            (["color_type"], ["CHOCOLATE"]),
            (
                ["name", "description"],
                ["extra new fake hedgehog name", "extra new fake hedgehog description"],
            ),
            (["age", "color_type"], [2.00, "CHOCOLATE"]),
        ),
    )
    async def test_update_hedgehog_with_valid_input(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_hedgehog: HedgehogInDB,
        attrs_to_change: List[str],
        values: List[str],
    ) -> None:
        hedgehog_update = {
            "hedgehog_update": {
                attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))
            }
        }
        res = await authorized_client.put(
            app.url_path_for(
                "hedgehogs:update-hedgehog-by-id", hedgehog_id=test_hedgehog.id
            ),
            json=hedgehog_update,
        )
        assert res.status_code == status.HTTP_200_OK
        updated_hedgehog = HedgehogInDB(**res.json())
        assert updated_hedgehog.id == test_hedgehog.id
        for i in range(len(attrs_to_change)):
            assert getattr(updated_hedgehog, attrs_to_change[i]) != getattr(
                test_hedgehog, attrs_to_change[i]
            )
            assert getattr(updated_hedgehog, attrs_to_change[i]) == values[i]

        for attr, value in updated_hedgehog.dict().items():
            if attr not in attrs_to_change and attr != "updated_at":
                assert getattr(test_hedgehog, attr) == value

    async def test_user_recieves_error_if_updating_other_users_hedgehog(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_hedgehogs_list: List[HedgehogInDB],
    ) -> None:
        res = await authorized_client.put(
            app.url_path_for(
                "hedgehogs:update-hedgehog-by-id", hedgehog_id=test_hedgehogs_list[0].id
            ),
            json={"hedgehog_update": {"age": 3.2}},
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_user_cant_change_ownership_of_hedgehog(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_hedgehog: HedgehogInDB,
        test_user: UserInDB,
        test_user2: UserInDB,
    ) -> None:
        res = await authorized_client.put(
            app.url_path_for(
                "hedgehogs:update-hedgehog-by-id", hedgehog_id=test_hedgehog.id
            ),
            json={"hedgehog_update": {"owner": test_user2.id}},
        )
        assert res.status_code == status.HTTP_200_OK
        hedgehog = HedgehogPublic(**res.json())
        assert hedgehog.owner == test_user.id

    @pytest.mark.parametrize(
        "id, payload, status_code",
        (
            (-1, {"name": "test"}, 422),
            (0, {"name": "test2"}, 422),
            (500, {"name": "test3"}, 404),
            (1, None, 422),
            (1, {"color_type": "invalid color type"}, 422),
            (1, {"color_type": None}, 400),
        ),
    )
    async def test_update_hedgehog_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        id: int,
        payload: Dict[str, Optional[str]],
        status_code: int,
    ) -> None:
        hedgehog_update = {"hedgehog_update": payload}
        res = await authorized_client.put(
            app.url_path_for("hedgehogs:update-hedgehog-by-id", hedgehog_id=id),
            json=hedgehog_update,
        )
        assert res.status_code == status_code


class TestDeleteHedgehog:
    async def test_can_delete_hedgehog_successfully(
        self, app: FastAPI, authorized_client: AsyncClient, test_hedgehog: HedgehogInDB
    ) -> None:
        res = await authorized_client.delete(
            app.url_path_for(
                "hedgehogs:delete-hedgehog-by-id", hedgehog_id=test_hedgehog.id
            )
        )
        assert res.status_code == status.HTTP_200_OK

    async def test_user_cant_delete_other_users_hedgehog(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_hedgehogs_list: List[HedgehogInDB],
    ) -> None:
        res = await authorized_client.delete(
            app.url_path_for(
                "hedgehogs:delete-hedgehog-by-id", hedgehog_id=test_hedgehogs_list[0].id
            )
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "id, status_code",
        ((5000000, 404), (0, 422), (-1, 422), (None, 422)),
    )
    async def test_wrong_id_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_hedgehog: HedgehogInDB,
        id: int,
        status_code: int,
    ) -> None:
        res = await authorized_client.delete(
            app.url_path_for("hedgehogs:delete-hedgehog-by-id", hedgehog_id=id)
        )
        assert res.status_code == status_code
