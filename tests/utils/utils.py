import random
import string

from fastapi.testclient import TestClient

from config.settings import settings

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=25))

def random_email() -> str:
    return "".join(f'{random_lower_string()}@{random_lower_string()}.com')

def random_phone_number() -> str:
    return f'+{"".join(random.choices(string.digits, k=random.randint(7, 19)))}'

def get_superuser_token_headers(client: TestClient) -> dict[str: str]:
    login_data = {
        "username": settings.SUPERUSER_USERNAME,
        "password": settings.SUPERUSER_PASSWORD
    }
    r = client.post(
        url=f'{settings.API_V1_STR}/login/access-token',
        data=login_data
    )
    token = r.json()
    access_token = token["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers