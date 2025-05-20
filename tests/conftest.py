from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from config.settings import settings
from config.db import engine, init_db
from core.main import app
from apps.Clients.models import Client
from apps.Users.models import User
from apps.Interactions.models import Interaction
from tests.utils.user import authenticate_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Interaction)
        session.exec(statement)
        statement = delete(Client)
        session.exec(statement)
        statement = delete(User)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def super_user_headers(client: TestClient) -> dict[str: str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_headers(client: TestClient, db: Session) -> dict[str: str]:
    return authenticate_token_from_email(
        client=client, username=settings.NORMAL_USER_USERNAME, db=db
    )
