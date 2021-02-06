from typing import List

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
        name='test hedgehog',
        description='test description',
        age=0.0,
        color_type='SOLT & PEPPER',
    )


class TestHedgehogsRoutes:
    async def test_routes_exist(
        self,
        app: FastAPI,
        client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for('hedgehogs:create-hedgehog'), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for('hedgehogs:create-hedgehog'), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateHedgehog:
    async def test_valid_input_creates_hedgehog(
        self, app: FastAPI, client: AsyncClient, new_hedgehog: HedgehogCreate
    ) -> None:
        res = await client.post(
            app.url_path_for('hedgehogs:create-hedgehog'),
            json={'new_hedgehog': new_hedgehog.dict()}
        )
        assert res.status_code == HTTP_201_CREATED
        created_hedgehog = HedgehogCreate(**res.json())
        assert created_hedgehog == new_hedgehog

    @pytest.mark.parametrize(
        'invalid_payload, status_code',
        (
            (None, 422),
            ({}, 422),
            ({'name': 'test_name'}, 422),
            ({'age': 2}, 422),
            ({'name': 'test_name', 'description': 'test'}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for('hedgehogs:create-hedgehog'),
            json={'new_hedgehog': invalid_payload}
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
            'hedgehogs:get-hedgehog-by-id',
            id=test_hedgehog.id
        ))
        assert res.status_code == HTTP_200_OK
        hedgehog = HedgehogInDB(**res.json())
        assert hedgehog == test_hedgehog

    @pytest.mark.parametrize(
        'id, status_code',
        (
            (500, 404),
            (-1, 404),
            (None, 422),
        ),
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, client: AsyncClient, id: int, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for('hedgehogs:get-hedgehog-by-id', id=id))
        assert res.status_code == status_code

    async def test_get_all_hedgehogs_returns_valid_response(
        self, app: FastAPI, client: AsyncClient, test_hedgehog: HedgehogInDB
    ) -> None:
        res = await client.get(app.url_path_for('hedgehogs:get-all-hedgehogs'))
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        hedgehogs = [HedgehogInDB(**item) for item in res.json()]
        assert test_hedgehog in hedgehogs


class TestUpdateHedgehog:
    @pytest.mark.parametrize('attrs_to_change, values',
                             ((['name'],
                               ['new fake hedgehog name']),
                              (['description'],
                               ['new fake hedgehog description']),
                              (['age'],
                               [3.14]),
                              (['color_type'],
                               ['CHOCOLATE']),
                              (['name', 'description'],
                               ['extra new fake hedgehog name',
                                'extra new fake hedgehog description']),
                              (['age', 'color_type'],
                               [2.00, 'CHOCOLATE']),),)
    async def test_update_hedgehog_with_valid_input(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_hedgehog: HedgehogInDB,
        attrs_to_change: List[str],
        values: List[str],
    ) -> None:
        hedgehog_update = {
            'hedgehog_update': {
                attrs_to_change[i]: values[i] for i in range(
                    len(attrs_to_change))}}
        res = await client.put(
            app.url_path_for('hedgehogs:update-hedgehog-by-id', id=test_hedgehog.id),
            json=hedgehog_update
        )
        assert res.status_code == HTTP_200_OK
        updated_hedgehog = HedgehogInDB(**res.json())
        assert updated_hedgehog.id == test_hedgehog.id

        for i in range(len(attrs_to_change)):
            assert getattr(
                updated_hedgehog,
                attrs_to_change[i]) != getattr(
                test_hedgehog,
                attrs_to_change[i])
            assert getattr(updated_hedgehog, attrs_to_change[i]) == values[i]

        for attr, value in updated_hedgehog.dict().items():
            if attr not in attrs_to_change:
                assert getattr(test_hedgehog, attr) == value

    @pytest.mark.parametrize(
        'id, payload, status_code',
        (
            (-1, {'name': 'test'}, 422),
            (0, {'name': 'test2'}, 422),
            (500, {'name': 'test3'}, 404),
            (1, None, 422),
            (1, {'color_type': 'invalid color type'}, 422),
            (1, {'color_type': None}, 400),
        ),
    )
    async def test_update_hedgehog_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: int,
        payload: dict,
        status_code: int,
    ) -> None:
        hedgehog_update = {'hedgehog_update': payload}
        res = await client.put(
            app.url_path_for('hedgehogs:update-hedgehog-by-id', id=id),
            json=hedgehog_update
        )
        assert res.status_code == status_code


class TestDeleteHedgehog:
    async def test_can_delete_hedgehog_successfully(
        self, app: FastAPI, client: AsyncClient, test_hedgehog: HedgehogInDB
    ) -> None:
        res = await client.delete(app.url_path_for(
            'hedgehogs:delete-hedgehog-by-id', id=test_hedgehog.id))
        assert res.status_code == HTTP_200_OK

        res = await client.get(app.url_path_for(
            'hedgehogs:get-hedgehog-by-id', id=test_hedgehog.id))
        assert res.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        'id, status_code',
        (
            (500, 404),
            (0, 422),
            (-1, 422),
            (None, 422),
        ),
    )
    async def test_delete_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: int,
        status_code: int
    ) -> None:
        res = await client.delete(app.url_path_for(
            'hedgehogs:delete-hedgehog-by-id', id=id))
        assert res.status_code == status_code
