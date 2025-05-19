import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import datetime, timezone, timedelta

from apps.Interactions.models import (
    InteractionType,
    InteractionStatus,
    ChannelType
)
from tests.utils.interaction import create_random_interaction
from tests.utils.client import create_random_client
from tests.utils.user import create_random_user
from config.settings import settings

BASE_URL = f'{settings.API_V1_STR}/interactions'


def test_create_interaction(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str],
) -> None:
    user = create_random_user(db)
    user_id = user.id
    new_client = create_random_client(db)
    client_id = new_client.id
    interaction_datetime = datetime.now(timezone.utc) - timedelta(days=1)
    data = {
        "client_id": str(client_id),
        "user_id": str(user_id),
        "interaction_type": InteractionType.meeting,
        "interaction_datetime": interaction_datetime,
        "channel": ChannelType.phone,
        "interaction_status": InteractionStatus.pending
    }
    response = client.post(
        url=BASE_URL,
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["client_id"] == data["client_id"]
    assert content["user_id"] == data["user_id"]
    assert content["interaction_type"] == data["interaction_type"]
    assert content["interaction_datetime"] == data["interaction_datetime"]
    assert content["channel"] == data["channel"]
    assert content["interaction_status"] == data["interaction_status"]
    assert "id" in content


def test_read_interaction(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    interaction = create_random_interaction(db)
    response = client.get(
        url=f"{BASE_URL}/{interaction.id}",
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["client_id"] == str(interaction.client_id)
    assert content["user_id"] == str(interaction.user_id)
    assert content["interaction_type"] == interaction.interaction_type
    assert content["interaction_datetime"] == interaction.interaction_datetime
    assert content["channel"] == interaction.channel
    assert content["interaction_status"] == interaction.interaction_status
    assert content["id"] == str(interaction.id)
    

def test_read_interaction_not_found(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    response = client.get(
        url=f"{BASE_URL}/{uuid.uuid4()}",
        headers=super_user_headers
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Interaction not found"
    

def test_read_interaction_not_enough_permission(
    client: TestClient,
    db: Session,
    normal_user_headers: dict[str: str]
) -> None: 
    interaction = create_random_interaction(db)
    response = client.get(
        url=F"{BASE_URL}/{interaction.id}",
        headers=normal_user_headers
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"
    

def test_read_interactions(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str]
) -> None:
    new_interaction1 = create_random_interaction(db)
    new_interaction2 = create_random_interaction(db)
    response = client.get(
        url=BASE_URL,
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    item = content["items"][0]
    assert content["total_count"] == 2
    assert "id" in item
    

def test_update_interaction(
    client: TestClient,
    super_user_headers: dict[str: str],
    db: Session
) -> None:
    new_interaction = create_random_interaction(db)
    user = create_random_user(db)
    user_id = user.id
    new_client = create_random_client(db)
    client_id = new_client.id
    interaction_datetime = datetime.now(timezone.utc) - timedelta(days=1)
    data = {
        "client_id": str(client_id),
        "user_id": str(user_id),
        "interaction_type": InteractionType.meeting,
        "interaction_datetime": interaction_datetime,
        "channel": ChannelType.phone,
        "interaction_status": InteractionStatus.pending
    }
    response = client.put(
        url=f"{BASE_URL}/{new_interaction.id}",
        headers=super_user_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["client_id"] == data["client_id"]
    assert content["user_id"] == data["user_id"]
    assert content["interaction_type"] == data["interaction_type"]
    assert content["interaction_datetime"] == data["interaction_datetime"]
    assert content["channel"] == data["channel"]
    assert content["interaction_status"] == data["interaction_status"]
    assert "id" in content


def test_update_interaction_not_found(
    client: TestClient,
    super_user_headers: dict[str: str],
) -> None:
    response = client.put(
        url=f'{BASE_URL}/{uuid.uuid4()}',
        headers=super_user_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content['detail'] == "Interaction not found"


def test_update_interaction_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    new_interaction = create_random_interaction(db)
    response = client.put(
        url=f'{BASE_URL}/{new_interaction.id}',
        headers=normal_user_headers,
        json={}
    )
    assert response.status_code == 400
    content = response.json()
    assert content['detail'] == "Not enough permission"
    

def test_delete_interaction(
    client: TestClient,
    db: Session,
    super_user_headers: dict[str: str]
) -> None:
    new_interaction = create_random_interaction(db)
    response = client.delete(
        url=f'{BASE_URL}/{new_interaction.id}',
        headers=super_user_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["detail"] == "Interaction was deleted successfully"


def test_delete_interaction_not_found(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    response = client.delete(
        url=f'{BASE_URL}/{uuid.uuid4()}',
        headers=super_user_headers
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Interaction not found"


def test_delete_interaction_not_enough_permission(
    client: TestClient,
    normal_user_headers: dict[str: str],
    db: Session
) -> None:
    new_interaction = create_random_interaction(db)
    response = client.delete(
        url=f'{BASE_URL}/{new_interaction.id}',
        headers=normal_user_headers
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permission"
