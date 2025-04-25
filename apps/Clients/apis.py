import uuid
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from apps.Clients.models import (
    ClientPublic,
    ClientCreate,
    ClientList,
    ClientUpdate,
    Client,
    Message
)
from config.settings import settings
from apps.deps import SessionDep
from config.utils import utcnow

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=ClientList)
def get_clients(
        session: SessionDep, skip: int = 0, limit: int = 100 
    ) -> ClientList:
    limit = min(limit, settings.MAX_LIMIT)
    # List of clients
    #TODO add checking for authentication
    count_statement = select(func.count()).select_from(Client)
    count = session.exec(count_statement).one()
    statement = select(Client).order_by(Client.created_at.desc()).offset(skip).limit(limit)
    clients = session.exec(statement).all()
    return ClientList(data=clients, count=count)


@router.get("/{id}", response_model=ClientPublic)
def get_client(
    session: SessionDep,
    id: uuid.UUID
) -> ClientPublic:
    #Get Client by id
    client = session.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=ClientPublic)
def create_client(
    session: SessionDep,
    client_in: ClientCreate,
) -> ClientCreate:
    client = Client.model_validate(client_in)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client
    


@router.put("/{id}", response_model=ClientPublic)
def update_client(
    session: SessionDep,
    client_in: ClientUpdate,
    id: uuid.UUID
) -> ClientPublic:
    client = session.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    update_dict = client_in.model_dump(exclude_unset=True)
    client.sqlmodel_update(update_dict)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.delete("/{id}", response_model=Message)
def delete_client(
    session: SessionDep,
    id: uuid.UUID
) -> Message:
    client = session.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    session.delete(client)
    session.commit()
    return Message(status=200, message="Client deleted successfully")