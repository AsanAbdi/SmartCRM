from sqlmodel import Session
from datetime import datetime, timezone, timedelta

from apps.Interactions.models import (
    Interaction,
    InteractionCreate,
    InteractionType,
    InteractionStatus,
    ChannelType
)
from tests.utils.user import create_random_user
from tests.utils.client import create_random_client


def create_random_interaction(db: Session) -> Interaction:
    user = create_random_user(db)
    user_id = user.id
    client = create_random_client(db)
    client_id = client.id
    interaction_datetime = datetime.now(timezone.utc) - timedelta(days=1)
    interaction_in = InteractionCreate(
        client_id=client_id,
        user_id=user_id,
        interaction_type=InteractionType.meeting,
        interaction_status=InteractionStatus.pending,
        channel=ChannelType.phone,
        interaction_datetime=interaction_datetime
    )
    interaction = Interaction.model_validate(interaction_in)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction