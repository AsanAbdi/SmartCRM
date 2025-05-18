from sqlmodel import Session

from apps.Clients.models import (
    Client, 
    ClientCreate,
    ClientSegment,
    ClientSource
)
from tests.utils.utils import random_lower_string, random_phone_number, random_email
from tests.utils.user import create_random_user


def create_random_client(db: Session) -> Client:
    user = create_random_user()
    assigned_to_id = user.id
    assert assigned_to_id is not None
    full_name = random_lower_string()
    phone_number = random_phone_number()
    email = random_email()
    client_in = ClientCreate(
        full_name=full_name, 
        email=email, 
        phone_number=phone_number, 
        source=ClientSource.other, 
        segment=ClientSegment.test,
        assigned_to=assigned_to_id
    )
    client = Client.model_validate(client_in)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
    