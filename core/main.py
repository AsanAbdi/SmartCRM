from fastapi import FastAPI

import sqlalchemy.types as types
types.DOUBLE = types.Float


from apps.Clients.apis import router as ClientRouter
from apps.Users.apis import router as UserRouter
from apps.Login.apis import router as LoginRouter
from config.settings import settings

app = FastAPI()

app.include_router(ClientRouter, prefix=settings.API_V1_STR)
app.include_router(UserRouter, prefix=settings.API_V1_STR)
app.include_router(LoginRouter, prefix=settings.API_V1_STR)
