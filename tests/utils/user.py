from venv import create
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from config.settings import settings
from apps.Users.models import User, UserCreate, UserUpdate
from tests.utils.utils import random_email, random_lower_string
from config.security import get_password_hash


def user_authentication_headers(
    client: TestClient, 
    username: str, 
    password: str
) -> dict[str: str]:
    login_data = {
        "username": username,
        "password": password
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    print(f"Login response: {r.json()}")
    tokens = r.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreate(email=email, password=password, username=username)
    db_obj = User.model_validate(user_in, update={"hashed_password": get_password_hash(user_in.password)})
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def authenticate_token_from_email(
    client:  TestClient,
    username: str,
    db: Session
) -> dict[str: str]:
    password = random_lower_string()
    email = random_email()
    user = db.exec(select(User).where(User.username==username)).first()
    if not user:
        password_hash = get_password_hash(password)  # Хешируем пароль
        user_in_create = UserCreate(
            username=username,
            email=email,
            password=password,
        )
        user_data = user_in_create.model_dump()
        user_data["hashed_password"] = password_hash  # Добавляем хешированный пароль
        user = User.model_validate(user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if not user.id:
            raise Exception("User id not set")
        password_hash = get_password_hash(password)
        user.hashed_password = password_hash
        db.add(user)
        db.commit()
        db.refresh(user)

    return user_authentication_headers(client=client, username=username, password=password)