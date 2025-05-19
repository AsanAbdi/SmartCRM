import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from apps.Clients.models import ClientSource, ClientSegment
from config.settings import settings
from tests.utils.user import create_random_user
from tests.utils.client import create_random_client
from tests.utils.utils import random_lower_string, random_email, random_phone_number

BASE_URL = f"{settings.API_V1_STR}/clients/"

def test_create_client(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    user = create_random_user(db)
    user_id = user.id
    data = {
        "full_name":  random_lower_string(),
        "email": random_email(),
        "phone_number": random_phone_number(),
        "source": ClientSource.other,
        "segment": ClientSegment.test,
        "assigned_to": str(user_id)
    }
    response = client.post(
        url=BASE_URL,
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["full_name"] == data["full_name"]
    assert content["email"] == data["email"]
    assert content["phone_number"] == data["phone_number"]
    assert content["source"] == data["source"]
    assert content["segment"] == data["segment"]
    assert content["assigned_to"] == data["assigned_to"]
    assert "id" in content


def test_read_client(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    new_client = create_random_client(db)
    response = client.get(
        url=f"{BASE_URL}/{new_client.id}",
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["full_name"] == new_client.full_name
    assert content["email"] == new_client.email
    assert content["phone_number"] == new_client.phone_number
    assert content["source"] == new_client.source
    assert content["segment"] == new_client.segment
    assert content["assigned_to"] == new_client.assigned_to
    
    
def test_read_client_not_found(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    response = client.get(
        url=f"{BASE_URL}/{uuid.uuid4()}",
        headers=super_user_headers
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Client not found"
    

def test_read_client_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    new_client = create_random_client(db)
    response = client.get(
        url=f"{BASE_URL}/{new_client.id}",
        headers=normal_user_headers
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"
    
    
def test_read_clients(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str]
) -> None:
    create_random_client(db)
    create_random_client(db)
    response = client.get(
        url=BASE_URL,
        headers=super_user_headers
    )
    assert response.satatus_code == 200
    content = response.json()
    assert content["total_count"] == 2
    

def test_read_clients_not_enough_permission(
    client: TestClient,
    db: Session,
    normal_user_headers: dict[str: str]
) -> None:
    create_random_client(db)
    create_random_client(db)
    response = client.get(
        url=BASE_URL,
        headers=normal_user_headers
    )
    assert response.satatus_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"


def test_update_client(
    client: TestClient,
    super_user_headers:  dict[str: str],
    db: Session
) -> None:
    user = create_random_user(db)
    user_id = user.id
    data = {
        "full_name":  random_lower_string(),
        "email": random_email(),
        "phone_number": random_phone_number(),
        "source": ClientSource.other,
        "segment": ClientSegment.test,
        "assigned_to": str(user_id)
    }
    new_client = create_random_client(db)
    response = client.put(
        url=f"{BASE_URL}/{new_client.id}",
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["full_name"] == data["full_name"]
    assert content["email"] == data["email"]
    assert content["phone_number"] == data["phone_number"]
    assert content["source"] == data["source"]
    assert content["segment"] == data["segment"]
    assert content["assigned_to"] == data["assigned_to"]
    

def test_udpate_client_not_found(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    user = create_random_user(db)
    user_id = user.id
    data = {
        "full_name":  random_lower_string(),
        "email": random_email(),
        "phone_number": random_phone_number(),
        "source": ClientSource.other,
        "segment": ClientSegment.test,
        "assigned_to": str(user_id)
    }
    response = client.put(
        url=f"{BASE_URL}/{uuid.uuid4()}",
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Client not found"
    

def test_udpate_client_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    data = {
        "full_name":  random_lower_string(),
        "email": random_email(),
        "phone_number": random_phone_number(),
        "source": ClientSource.other,
        "segment": ClientSegment.test,
    }
    new_client = create_random_client(db)
    response = client.put(
        url=f"{BASE_URL}/{new_client.id}",
        headers=normal_user_headers,
        json=data
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"


def test_delete_client(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    new_client = create_random_client(db)
    response = client.delete(
        url=f"{BASE_URL}/{new_client.id}",
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["detail"] == "Client was successfully deleted"


def test_delete_client_not_found(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    response = client.delete(
        url=f"{BASE_URL}/{uuid.uuid4()}",
        headers=super_user_headers
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Client not found"


def test_delete_client_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    new_client = create_random_client(db)
    response = client.delete(
        url=f'{BASE_URL}/{new_client.id}',
        headers=normal_user_headers
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"
