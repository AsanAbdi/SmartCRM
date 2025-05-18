from config.settings import settings
from sqlmodel import create_engine, select, Session

from apps.Users.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.username == settings.SUPERUSER_USERNAME)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.SUPERUSER_EMAIL,
            username=settings.SUPERUSER_USERNAME,
            password=settings.SUPERUSER_PASSWORD,
            
        )
        user = User.model_validate(user_in)
        session.add(user)
        session.commit()
        session.refresh(user)