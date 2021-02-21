import os
import subprocess
import uuid
import warnings

import alembic
import docker as pydocker
import pytest
from alembic.config import Config
from app.db.repositories.hedgehogs import HedgehogsRepository
from app.db.repositories.users import UsersRepository
from app.models.hedgehog import HedgehogCreate, HedgehogInDB
from app.models.user import UserCreate, UserInDB
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from tests.utility import ping_postgres

config = Config("alembic.ini")


@pytest.fixture(scope="session")
def docker() -> pydocker.APIClient:
    # base url is the unix socket we use to communicate with docker
    return pydocker.APIClient(base_url="unix://var/run/docker.sock", version="auto")


@pytest.fixture(scope="session", autouse=True)
def postgres_container(docker: pydocker.APIClient) -> None:
    """
    Use docker to spin up a postgres container for the duration of the testing session.
    Kill it as soon as all tests are run.
    DB actions persist across the entirety of the testing session.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    image = "postgres:12.1-alpine"
    docker.pull(image)

    # create the new container using
    # the same image used by our database
    command = """head -1 /proc/self/cgroup|cut -d/ -f3"""
    bin_own_container_id = subprocess.check_output(['sh', '-c', command])
    own_container_id = bin_own_container_id.decode().replace('\n', '')
    inspection = docker.inspect_container(own_container_id)

    network = list(inspection["NetworkSettings"]["Networks"].keys())[0]
    networking_config = docker.create_networking_config({
        network: docker.create_endpoint_config()
    })

    container_name = f"test-postgres-{uuid.uuid4()}"
    container = docker.create_container(
        image=image,
        name=container_name,
        detach=True,
        networking_config=networking_config
    )
    docker.start(container=container["Id"])

    inspection = docker.inspect_container(container["Id"])
    ip_address = inspection['NetworkSettings']['Networks'][network]['IPAddress']
    dsn = f"postgresql://postgres:postgres@{ip_address}/postgres"

    try:
        ping_postgres(dsn)
        os.environ['CONTAINER_DSN'] = dsn
        alembic.command.upgrade(config, "head")
        yield container
    finally:
        docker.kill(container["Id"])
        docker.remove_container(container["Id"])


@pytest.fixture
def app() -> FastAPI:
    from app.api.server import get_application
    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest.fixture
async def test_hedgehog(db: Database) -> HedgehogInDB:
    hedgehog_repo = HedgehogsRepository(db)
    new_hedgehog = HedgehogCreate(
        name="fake hedgehog name",
        description="fake description",
        age=2.2,
        color_type="SOLT & PEPPER",
    )
    return await hedgehog_repo.create_hedgehog(new_hedgehog=new_hedgehog)

@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="nmomos@mail.com",
        username="nmomoishedgehog",
        password="nmomosissocute",
    )
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)
