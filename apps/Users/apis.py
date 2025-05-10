from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select, func
from uuid import UUID, uuid4

from apps.deps import SessionDep
from config.settings import settings
from config.utils import utcnow_date
from apps.Users.models import (
    User,
    UserCreate,
    UserUpdate,
    UserList,
    UserPublic
)
from config.security import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"], )


@router.get("/", response_model=UserList)
def get_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100
) -> UserList:
    limit = min(limit, settings.MAX_LIMIT)
    #TODO add checking for authentication
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()
    users_statement = select(User).order_by(User.date_joined.desc()).offset(skip).limit(limit)
    users = session.exec(users_statement).all()
    return UserList(items=users, total_count=count)


@router.get("/{id}", response_model=UserPublic)
def get_user(
    session: SessionDep,
    id: UUID
) -> UserPublic:
    user = session.get(User, id)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    return user


@router.post("/", response_model=UserPublic)
def create_user(
    session: SessionDep,
    user_in: UserCreate,
) -> UserPublic:
    if session.exec(select(User).where((User.email == user_in.email))).first() or session.exec(select(User).where((User.username == user_in.username))).first():
        raise HTTPException(status_code=409, detail="User with same email or username already exists")
    data = user_in.model_dump()
    print(data, "ХУЙ ЕГО ЧТО ЕЩЁ")
    user = User(
        id=uuid4(),
        hashed_password=get_password_hash(data.pop("password")),
        **data
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/{id}", response_model=UserPublic)
def update_user(
    session: SessionDep,
    user_in: UserUpdate,
    id: UUID
) -> UserPublic:
    user = session.get(User, id)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    update_dict = user_in.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_dict)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{id}")
def delete_user(
    session: SessionDep,
    id: UUID,
) -> JSONResponse:
    user = session.get(User, id)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    session.delete(user)
    session.commit()
    return JSONResponse(content={"response": "User was successfully deleted"}, status_code=200)