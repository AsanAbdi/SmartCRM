from fastapi.testclient import TestClient

from config.settings import settings
from tests.utils.utils import random_lower_string

BASE_URL = f'{settings.API_V1_STR}/login/access-token/'

def test_get_token(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    response = client.post(
        url=BASE_URL,
        headers=super_user_headers,
        data={
            "username": settings.SUPERUSER_USERNAME, 
            "password": settings.SUPERUSER_PASSWORD
        }
    )
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    

def test_get_token_wrong_password(
    client: TestClient,
    super_user_headers: dict[str: str]
) -> None:
    wrong_pass = random_lower_string()
    response = client.post(
        url=BASE_URL,
        headers=super_user_headers,
        data={
            "username": settings.SUPERUSER_USERNAME,
            "password": wrong_pass
        }
    )
    assert response.status_code == 400