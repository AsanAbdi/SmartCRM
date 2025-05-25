from uuid import uuid4
import uuid
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    status,
    Body,
    Query,
    Path
)
from fastapi.responses import JSONResponse
from sqlmodel import select, func
from typing import Annotated

from apps.Clients.models import (
    ClientPublic,
    ClientCreate,
    ClientList,
    ClientUpdate,
    Client
)
from config.settings import settings
from apps.deps import SessionDep, get_current_user
from apps.Users.models import User, UserRole
from config.utils import utcnow_time
from apps.utils import PERMISSION_EXCEPTION

router = APIRouter(prefix="/clients", tags=["clients"])

NOT_EXISTING_ASSIGNED_TO = HTTPException(
    detail="User that you assigned to does not exist",
    status_code=status.HTTP_400_BAD_REQUEST
)

@router.get("/", response_model=ClientList)
def get_clients(
    session: SessionDep, 
    current_user: Annotated[User, Depends(get_current_user)],
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100
) -> ClientList:
    if current_user.role != UserRole.admin:
        raise PERMISSION_EXCEPTION
    limit = min(limit, settings.MAX_LIMIT)
    count_statement = select(func.count()).select_from(Client)
    count = session.exec(count_statement).one()
    statement = select(Client).order_by(Client.created_at.desc()).offset(skip).limit(limit)
    clients = session.exec(statement).all()
    return ClientList(items=clients, total_count=count)


@router.get("/{id}", response_model=ClientPublic)
def get_client(
    session: SessionDep, 
    id: Annotated[uuid.UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> ClientPublic:
    client = session.get(Client, id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if current_user.role != UserRole.admin and client.assigned_to is not None:
        if client.assigned_to != current_user.id:
            raise PERMISSION_EXCEPTION
    return client


@router.post("/", response_model=ClientPublic)
def create_client(
    session: SessionDep, 
    client_in: Annotated[ClientCreate, Body()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> ClientPublic:
    if session.exec(select(Client).where(Client.email == client_in.email)).first() or session.exec(select(Client).where(Client.phone_number == client_in.phone_number)).first():
        raise HTTPException(detail="Client with this email or phone number already exists", status_code=status.HTTP_409_CONFLICT)
    if client_in.assigned_to is not None:
        user = session.get(User, client_in.assigned_to)
        if not user:
            raise NOT_EXISTING_ASSIGNED_TO
    client = Client(
        id=uuid4(),
        created_at=utcnow_time(),
        is_active=True,
        **client_in.model_dump(),
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return client



@router.put("/{id}", response_model=ClientPublic)
def update_client(
    session: SessionDep, 
    client_in: Annotated[ClientUpdate, Body()],
    id: Annotated[uuid.UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> ClientPublic:
    client = session.get(Client, id)
    if not client:
        raise HTTPException(detail="Client not found", status_code=status.HTTP_404_NOT_FOUND)
    if client.assigned_to is not None and current_user.role != UserRole.admin:
        if client.assigned_to != current_user.id:
            raise PERMISSION_EXCEPTION
    update_dict = client_in.model_dump(exclude_unset=True)
    client.sqlmodel_update(update_dict)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.delete("/{id}")
def delete_client(
    session: SessionDep, 
    id: Annotated[uuid.UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    client = session.get(Client, id)
    if not client:
        raise HTTPException(detail="Client not found", status_code=status.HTTP_404_NOT_FOUND)
    if client.assigned_to is not None and current_user.role != UserRole.admin:
        if client.assigned_to != current_user.id:
            raise PERMISSION_EXCEPTION
    session.delete(client)
    session.commit()
    return JSONResponse(content={"detail": "Client was successfully deleted"}, status_code=status.HTTP_200_OK)