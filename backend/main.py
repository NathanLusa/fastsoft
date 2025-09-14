from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from components import get_example, get_simple_example
from dynamic_crud import DynamicCRUDManager, FieldConfig, DynamicCRUDConfig, engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager # Import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Create tables
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown logic (if any)


templates = Jinja2Templates(directory="backend/templates")

app = FastAPI(lifespan=lifespan) # Pass the lifespan function to FastAPI
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Dynamic CRUD Manager
crud_manager = DynamicCRUDManager(app)

# # Define a User resource
user_config = DynamicCRUDConfig(
    resource_name="User",
    table_name="users", # Optional, defaults to "users"
    fields=[
        FieldConfig(name="id", type="int", primary_key=True, hidden=True),
        FieldConfig(name="name", type="str", max_length=100, nullable=False, label="Nome"),
        # FieldConfig(name="email", type="str", unique=True, nullable=False, label="Email"),
        # FieldConfig(name="age", type="int", nullable=True, label="Idade"),
        # FieldConfig(name="is_active", type="bool", default=True, label="Ativo"),
        # FieldConfig(name="created_at", type="datetime", default="now", read_only=True, label="Criado Em"),
    ],
    form_title="Gerenciar Usuário",
    form_submit_button_text="Salvar Usuário",
    form_cancel_button_text="Voltar",
    router_kwargs={"prefix": "/api/users_dynamic"}, # Custom API prefix for this resource
)

# Register the User resource
crud_manager.register_resource(user_config)



@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@app.get("/api/components")
def read_item():
    return get_example()

@app.get("/api/components/simple")
def read_simple_item():
    return get_simple_example()

@app.get("/api/components/user")
def read_simple_item():
    user_resource = crud_manager.get_resource("User")
    form_json = user_resource["form_generator"].generate_form().to_json()
    return form_json


# Dynamic form endpoint for User resource
@app.get("/forms/users", response_class=HTMLResponse, include_in_schema=False)
async def get_user_form(request: Request):
    user_resource = crud_manager.get_resource("User")
    form_json = user_resource["form_generator"].generate_form().to_json()
    return templates.TemplateResponse(
        request=request, name="dynamic_form.html", context={"form_data": form_json}
    )