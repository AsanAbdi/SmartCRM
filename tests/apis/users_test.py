import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.utils import random_lower_string, random_email
from tests.utils.user import create_random_user
from config.settings import settings

BASE_URL = f'{settings.API_V1_STR}/users'


def test_create_user(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str],
) -> None:
    data = {
        "email": random_email(),
        "username": random_lower_string(),
        "password": random_lower_string()
    }
    response = client.post(
        url=BASE_URL,
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert content["username"] == data["username"]
    assert "id" in content
    assert "date_joined" in content


def test_read_user(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    user = create_random_user(db)
    response = client.get(
        url=f"{BASE_URL}/{user.id}",
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == user.email
    assert content["username"] == user.username
    assert "id" in content
    assert "date_joined" in content
    

def test_read_user_not_found(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    response = client.get(
        url=f"{BASE_URL}/{uuid.uuid4()}",
        headers=super_user_headers
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "User not found"
    

def test_read_user_not_enough_permission(
    client: TestClient,
    db: Session,
    normal_user_headers: dict[str: str]
) -> None: 
    user = create_random_user(db)
    response = client.get(
        url=F"{BASE_URL}/{user.id}",
        headers=normal_user_headers
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"
    

def test_read_users(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str]
) -> None:
    new_user1 = create_random_user(db)
    new_user2 = create_random_user(db)
    response = client.get(
        url=BASE_URL,
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    item = content["items"][0]
    assert content["total_count"] == 2
    assert "id" in item
    

def test_update_user(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    new_user = create_random_user(db)
    data = {
        "email": random_email(),
        "username": random_lower_string(),
        "password": random_lower_string()
    }
    response = client.put(
        url=f"{BASE_URL}/{new_user.id}",
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == new_user.email
    assert content["username"] == new_user.username
    assert "id" in content
    assert "date_joined" in content


def test_update_user_not_found(
    client: TestClient,
    super_user_headers: dict[str: str],
) -> None:
    response = client.put(
        url=f'{BASE_URL}/{uuid.uuid4()}',
        headers=super_user_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content['detail'] == "User not found"


def test_update_user_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    new_user = create_random_user(db)
    response = client.put(
        url=f'{BASE_URL}/{new_user.id}',
        headers=normal_user_headers,
        json={}
    )
    assert response.status_code == 400
    content = response.json()
    assert content['detail'] == "Not enough permission"
    

def test_delete_user(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str]
) -> None:
    new_user = create_random_user(db)
    response = client.delete(
        url=f'{BASE_URL}/{new_user.id}',
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["detail"] == "User was deleted successfully"


def test_delete_user_not_found(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    response = client.delete(
        url=f'{BASE_URL}/{uuid.uuid4()}',
        headers=super_user_headers
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Гser not found"


def test_delete_user_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    new_user = create_random_user(db)
    response = client.delete(
        url=f'{BASE_URL}/{new_user.id}',
        headers=normal_user_headers
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"
