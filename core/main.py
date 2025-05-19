from fastapi import FastAPI
from sqladmin import Admin, ModelView
import sqlalchemy.types as types
types.DOUBLE = types.Float

from config.db import engine

from apps.Clients.apis import router as ClientRouter
from apps.Users.apis import router as UserRouter
from apps.Login.apis import router as LoginRouter
from apps.Interactions.apis import router as InteractionRouter
from config.settings import settings
from apps.Clients.models import Client
from apps.Users.models import User
from apps.Interactions.models import Interaction

app = FastAPI()
admin = Admin(app, engine)

app.include_router(ClientRouter, prefix=settings.API_V1_STR)
app.include_router(UserRouter, prefix=settings.API_V1_STR)
app.include_router(LoginRouter, prefix=settings.API_V1_STR)
app.include_router(InteractionRouter, prefix=settings.API_V1_STR)

class ClientAdmin(ModelView, model=Client):
    column_list = [Client.id, Client.full_name, Client.email]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]
    
class InteractionAdmin(ModelView, model=Interaction):
    column_list = [Interaction.id, Interaction.interaction_status, Interaction.interaction_datetime]

admin.add_view(ClientAdmin)
admin.add_view(UserAdmin)
admin.add_view(InteractionAdmin)
#TODO rewrite all query\path params to Annotated
#TODO Refactor all files and whole code, to normal annotations and logic holes
#TODO make email verification after registration
#TODO in clients endpoints need to add verification is the user that making requests the one who is "assigned_to"