import pytest
from app.db.repositories.users import UsersRepository
from app.models.user import UserInDB
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

pytestmark = pytest.mark.asyncio


class TestUserRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        new_user = {
            "email": "test@email.io",
            "username": "test_username",
            "password": "testpassword"}
        res = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user})
        assert res.status_code != HTTP_404_NOT_FOUND


class TestUserRegistration:
    async def test_users_can_register_successfully(
        self, app: FastAPI, client: AsyncClient, db: Database,
    ) -> None:
        user_repo = UsersRepository(db)
        new_user = {
            "email": "foo@bar.com",
            "username": "foobar",
            "password": "bazquxquux"}

        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is None

        res = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user})
        assert res.status_code == HTTP_201_CREATED

        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.email == new_user["email"]
        assert user_in_db.username == new_user["username"]

        created_user = UserInDB(
            **res.json(),
            password="whatever",
            salt="123").dict(
            exclude={
                "password",
                "salt"})
        assert created_user == user_in_db.dict(exclude={"password", "salt"})

    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("email", "foo@bar.com", 400),
            ("username", "foobar", 400),
            ("email", "invalid_email@one@two.com", 422),
            ("password", "short", 422),
            ("username", "foobar@#$%^<>", 422),
            ("username", "ab", 422),
        ),
    )
    async def test_user_registration_fails_when_credentials_are_taken(
        self,
        app: FastAPI,
        client: AsyncClient,
        attr: str,
        value: str,
        status_code: int,
    ) -> None:
        new_user = {
            "email": "nottaken@email.com",
            "username": "not_taken_username",
            "password": "foobarpassword"}
        new_user[attr] = value

        res = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user})
        assert res.status_code == status_code
