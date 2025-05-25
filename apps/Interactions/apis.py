from fastapi import (
    APIRouter, 
    status, 
    HTTPException, 
    Depends,
    Body,
    Path,
    Query
)
from fastapi.responses import JSONResponse
from sqlmodel import select, func
from uuid import UUID, uuid4
from typing import Annotated

from apps.Clients.apis import UserRole
from apps.Interactions.models import (
    Interaction,
    InteractionCreate,
    InteractionList,
    InteractionPublic,
    InteractionUpdate
)
from config.settings import settings
from apps.Users.models import User
from apps.deps import SessionDep, get_current_user
from apps.utils import PERMISSION_EXCEPTION


router = APIRouter(prefix="/interactions", tags=["interaction"])

@router.get("/", response_model=InteractionList)
def get_interactions(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100
) -> InteractionPublic:
    if current_user.role != UserRole.admin:
        raise PERMISSION_EXCEPTION
    limit = min(limit, settings.MAX_LIMIT)
    interactions = session.exec(select(Interaction).order_by(Interaction.created_at).offset(skip).limit(limit))
    count = session.exec(select(func.count()).select_from((Interaction))).one()
    return InteractionList(
        items=interactions,
        total_count=count
    )
    

@router.get("/{id}", response_model=InteractionPublic)
def get_interaction(
    session: SessionDep,
    id: Annotated[UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> InteractionPublic:
    interaction = session.get(Interaction, id)
    if not interaction:
        raise HTTPException(detail="Interaction not found", status_code=status.HTTP_404_NOT_FOUND)
    if not interaction.is_active:
        raise HTTPException(detail="Interaction is inactive", status_code=status.HTTP_409_CONFLICT)
    if current_user.id != interaction.user_id and current_user.role != UserRole.admin:
        raise PERMISSION_EXCEPTION
    return interaction


@router.post("/", response_model=InteractionPublic)
def create_interaction(
    session: SessionDep,
    interaction_in: Annotated[InteractionCreate, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
) -> InteractionPublic:
    data = interaction_in.model_dump()
    interaction = Interaction(
        id = uuid4(),
        **data
    )
    session.add(interaction)
    session.commit()
    session.refresh(interaction)
    return interaction


@router.put("/{id}", response_model=InteractionPublic)
def update_interaction(
    session: SessionDep,
    interaction_in: Annotated[InteractionUpdate, Body()],
    id: Annotated[UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> InteractionPublic:
    interaction = session.get(Interaction, id)
    if not interaction:
        raise HTTPException(detail="Interaction not found", status_code=status.HTTP_404_NOT_FOUND)
    if current_user.id != interaction.user_id and current_user.role != UserRole.admin:
        raise PERMISSION_EXCEPTION
    data = interaction_in.model_dump(exclude_unset=True)
    interaction.sqlmodel_update(data)
    session.add(interaction)
    session.commit()
    session.refresh(interaction)
    return interaction


@router.delete("/{id}")
def delete_interaction(
    session: SessionDep,
    id: Annotated[UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    interaction = session.get(Interaction, id)
    if not interaction:
        raise HTTPException(detail="Interaction not found", status_code=status.HTTP_404_NOT_FOUND)
    if current_user.id != interaction.user_id and current_user.role != UserRole.admin:
        raise PERMISSION_EXCEPTION
    session.delete(interaction)
    session.commit()
    return JSONResponse(content={"detail": "Interaction was deleted successfully"}, status_code=status.HTTP_200_OK)