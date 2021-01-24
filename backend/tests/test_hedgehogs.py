import pytest
from app.models.hedgehog import HedgehogCreate, HedgehogInDB
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_404_NOT_FOUND,
                              HTTP_422_UNPROCESSABLE_ENTITY)

pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_hedgehog():
    return HedgehogCreate(
        name="test hedgehog",
        description="test description",
        age=0.0,
        color_type="SOLT & PEPPER",
    )


class TestHedgehogsRoutes:
    async def test_routes_exist(
        self,
        app: FastAPI,
        client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("hedgehogs:create-hedgehog"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("hedgehogs:create-hedgehog"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateHedgehog:
    async def test_valid_input_creates_hedgehog(
        self, app: FastAPI, client: AsyncClient, new_hedgehog: HedgehogCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("hedgehogs:create-hedgehog"),
            json={"new_hedgehog": new_hedgehog.dict()}
        )
        assert res.status_code == HTTP_201_CREATED
        created_hedgehog = HedgehogCreate(**res.json())
        assert created_hedgehog == new_hedgehog

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
        self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("hedgehogs:create-hedgehog"),
            json={"new_hedgehog": invalid_payload}
        )
        assert res.status_code == status_code


class TestGetHedgehog:
    async def test_get_hedgehog_by_id(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_hedgehog: HedgehogInDB
    ) -> None:
        res = await client.get(app.url_path_for(
            "hedgehogs:get-hedgehog-by-id",
            id=test_hedgehog.id
        ))
        assert res.status_code == HTTP_200_OK
        hedgehog = HedgehogInDB(**res.json())
        assert hedgehog == test_hedgehog

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (500, 404),
            (-1, 404),
            (None, 422),
        ),
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, client: AsyncClient, id: int, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for("hedgehogs:get-hedgehog-by-id", id=id))
        assert res.status_code == status_code
