from fastapi import FastAPI

import sqlalchemy.types as types
types.DOUBLE = types.Float


from apps.Clients.apis import router as ClientRouter
from config.settings import settings

app = FastAPI()

app.include_router(ClientRouter, prefix=settings.API_V1_STR)