from typing import Any, Callable, Dict, List, Optional, Type, Union

from fastapi import APIRouter, Depends, HTTPException, status, FastAPI # Import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, create_model # Keep Pydantic BaseModel for schemas
from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy.sql.schema import Column # Import Column
from sqlalchemy.sql.sqltypes import Text # Import Text
import datetime

from components import (
    Button, Checkbox, Div, Form, Heading, Input, InputLabel,
    Label, Page, Select, Span, Textarea, BaseComponent, StyleProvider
)

# --- Database Setup (can be customized) ---
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    with Session(engine) as session:
        yield session

# --- Field Type Mapping (SQLModel uses Python types directly) ---
PYTHON_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "datetime": datetime.datetime,
    "text": str, # For Textarea
    "enum": str, # For Select with options
}

# SQLModel handles types more directly, so this map is less critical for Field definitions
# But we keep it for reference or custom type handling if needed.
SQLMODEL_FIELD_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "datetime": datetime.datetime,
    "text": str,
    "enum": str,
}

COMPONENT_TYPE_MAP = {
    "str": "input",
    "int": "input",
    "float": "input",
    "bool": "checkbox",
    "datetime": "input",
    "text": "textarea",
    "enum": "select",
}

INPUT_HTML_TYPE_MAP = {
    "str": "text",
    "int": "number",
    "float": "number",
    "datetime": "datetime-local",
}

# --- Dynamic CRUD Configuration ---
class FieldConfig(BaseModel):
    name: str
    type: str # Python type hint as string (e.g., "str", "int", "bool")
    default: Any = None
    nullable: bool = True # For SQLModel, maps to Field(nullable=...)
    primary_key: bool = False
    index: bool = False
    unique: bool = False
    max_length: Optional[int] = None # For String(max_length=...)
    min_length: Optional[int] = None
    placeholder: Optional[str] = None
    label: Optional[str] = None
    component_type: Optional[str] = None # Override default component mapping
    input_html_type: Optional[str] = None # Override default HTML input type
    options: Optional[Dict[str, str]] = None # For 'enum' types: {"value": "Label"}
    read_only: bool = False
    hidden: bool = False
    
    # Customization points for form component
    form_component_kwargs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Keyword arguments to pass directly to the backend.components form component."
    )
    
    # Customization points for SQLModel Field
    sqlmodel_field_kwargs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Keyword arguments to pass directly to SQLModel Field."
    )
    
    # Customization points for Pydantic Field in schemas
    pydantic_field_kwargs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Keyword arguments to pass directly to Pydantic Field for schema generation."
    )

class DynamicCRUDConfig(BaseModel):
    resource_name: str # e.g., "User", "Product"
    table_name: Optional[str] = None # defaults to resource_name.lower() + "s"
    fields: List[FieldConfig]
    
    # Customization points
    base_model_class: Type[SQLModel] = SQLModel # Allow custom SQLModel base
    db_session_dependency: Callable[..., Session] = get_db
    
    # Customization for API endpoints
    api_prefix: Optional[str] = None # defaults to /api/{table_name}
    
    # FastAPI router customization
    router_kwargs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Keyword arguments to pass directly to APIRouter."
    )

    # Customization for Form generation
    form_title: Optional[str] = None # defaults to "Create {resource_name}"
    form_layout_class: str = "max-w-2xl mx-auto p-6 space-y-6"
    form_submit_button_text: str = "Submit"
    form_submit_button_class: str = "px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
    form_cancel_button_text: str = "Cancel"
    form_cancel_button_class: str = "px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
    
    # Allow overriding default component mapping
    component_map: Optional[Dict[str, str]] = None
    
    # Allow adding extra components to the form
    extra_form_components: Optional[List[Dict[str, Any]]] = None # JSON-like representation of components

# --- Dynamic SQLModel Generation ---
def generate_sqlmodel(config: DynamicCRUDConfig) -> Type[SQLModel]:
    table_name = config.table_name or f"{config.resource_name.lower()}s"
    model_name = config.resource_name
    
    # Build the class namespace with proper annotations
    class_namespace = {"__tablename__": table_name}
    
    # Add type annotations to the namespace
    annotations = {}
    
    for field in config.fields:
        py_type = PYTHON_TYPE_MAP.get(field.type)
        if py_type is None:
            raise ValueError(f"Unknown Python type for field '{field.name}': {field.type}")
        
        # Determine type annotation
        if field.primary_key or field.nullable:
            type_annotation = Optional[py_type]
        else:
            type_annotation = py_type
        
        # Store the annotation
        annotations[field.name] = type_annotation
        
        # Build Field arguments
        field_kwargs = {
            "primary_key": field.primary_key,
            "nullable": field.nullable,
            "index": field.index,
            "unique": field.unique,
        }
        
        # Handle default values
        if field.default is not None:
            if field.type == "datetime" and field.default == "now":
                field_kwargs["default_factory"] = datetime.datetime.now
            else:
                field_kwargs["default"] = field.default
        elif not field.nullable and not field.primary_key:
            # Required field without default - use Ellipsis
            field_kwargs["default"] = ...
        
        # Handle max_length for strings
        if field.type == "str" and field.max_length:
            field_kwargs["max_length"] = field.max_length
        elif field.type == "text":
            field_kwargs["sa_column"] = Column(Text)
            field_kwargs.pop("nullable", None)
        
        # Add any custom SQLModel field kwargs
        field_kwargs.update(field.sqlmodel_field_kwargs)
        
        # Create the field
        class_namespace[field.name] = Field(**field_kwargs)
    
    # Add annotations to the namespace
    class_namespace["__annotations__"] = annotations
    
    # Create the model class
    return type(model_name, (config.base_model_class,), class_namespace)

# --- Dynamic Pydantic Schema Generation ---
def generate_pydantic_schemas(config: DynamicCRUDConfig, sql_model: Type[SQLModel]) -> Dict[str, Type[BaseModel]]:
    schemas = {}
    
    def create_field_definition(field_config: FieldConfig, for_creation: bool = False, for_update: bool = False) -> tuple:
        """Create a field definition tuple for Pydantic create_model"""
        py_type = PYTHON_TYPE_MAP.get(field_config.type)
        if py_type is None:
            raise ValueError(f"Unknown Python type for field '{field_config.name}': {field_config.type}")
        
        # Determine type annotation
        if field_config.primary_key or field_config.nullable or for_update:
            type_annotation = Optional[py_type]
        else:
            type_annotation = py_type
        
        # Build Field arguments
        field_kwargs = field_config.pydantic_field_kwargs.copy()
        
        # Determine default value
        if field_config.primary_key:
            field_kwargs["default"] = None
        elif for_update:
            field_kwargs["default"] = None
        elif not field_config.nullable and not for_creation:
            # Required field for base schema
            if field_config.default is not None:
                field_kwargs["default"] = field_config.default
            else:
                field_kwargs["default"] = ...
        elif not field_config.nullable and for_creation:
            # Required field for creation
            if field_config.default is not None:
                field_kwargs["default"] = field_config.default
            else:
                field_kwargs["default"] = ...
        else:
            # Optional field
            field_kwargs["default"] = None
        
        return (type_annotation, Field(**field_kwargs))
    
    # Base Schema (for reading data from DB and response models)
    base_fields = {}
    for field_config in config.fields:
        if field_config.hidden and not field_config.primary_key:
            continue
        base_fields[field_config.name] = create_field_definition(field_config, for_creation=False)
    
    BaseSchema = create_model(f"{config.resource_name}Base", **base_fields)
    
    class Config:
        orm_mode = True
    BaseSchema.Config = Config
    schemas["Base"] = BaseSchema
    
    # Create Schema (for creating new data)
    create_fields = {}
    for field_config in config.fields:
        if field_config.primary_key or field_config.read_only or field_config.hidden:
            continue
        create_fields[field_config.name] = create_field_definition(field_config, for_creation=True)
    
    schemas["Create"] = create_model(f"{config.resource_name}Create", **create_fields)
    
    # Update Schema (for updating existing data)
    update_fields = {}
    for field_config in config.fields:
        if field_config.primary_key or field_config.read_only or field_config.hidden:
            continue
        update_fields[field_config.name] = create_field_definition(field_config, for_update=True)
    
    schemas["Update"] = create_model(f"{config.resource_name}Update", **update_fields)
    
    return schemas

# --- Dynamic Form Generation (No changes needed here from previous refactor) ---
class DynamicFormGenerator:
    def __init__(self, config: DynamicCRUDConfig, style_provider: Optional[StyleProvider] = None):
        self.config = config
        self.style_provider = style_provider or StyleProvider()
        self._component_map = COMPONENT_TYPE_MAP.copy()
        if self.config.component_map:
            self._component_map.update(self.config.component_map)
    
    def _get_form_component(self, field_config: FieldConfig) -> BaseComponent:
        component_type = field_config.component_type or self._component_map.get(field_config.type)
        if not component_type:
            raise ValueError(f"No component type defined for field type: {field_config.type}")
        
        common_kwargs = {
            "id": field_config.name,
            "name": field_config.name,
            "label": field_config.label or field_config.name.replace("_", " ").title(),
            "required": not field_config.nullable,
            "content": field_config.default if field_config.default is not None else "",
            **field_config.form_component_kwargs
        }
        
        if field_config.read_only:
            common_kwargs["readonly"] = True
        if field_config.hidden:
            common_kwargs["hidden"] = True

        if component_type == "input":
            input_type = field_config.input_html_type or INPUT_HTML_TYPE_MAP.get(field_config.type, "text")
            return InputLabel(
                type=input_type,
                placeholder=field_config.placeholder,
                max_length=field_config.max_length,
                min_length=field_config.min_length,
                **common_kwargs
            )
        elif component_type == "textarea":
            return InputLabel(
                type="textarea", # InputLabel handles textarea if type is 'textarea'
                placeholder=field_config.placeholder,
                max_length=field_config.max_length,
                min_length=field_config.min_length,
                **common_kwargs
            )
        elif component_type == "select":
            select = Select(
                id=common_kwargs["id"],
                name=common_kwargs["name"],
                required=common_kwargs["required"],
                **field_config.form_component_kwargs
            )
            if field_config.options:
                for value, label in field_config.options.items():
                    select.add_option(value, label)
            return Div(components=[
                Label(content=common_kwargs["label"], html_for=common_kwargs["id"]),
                select
            ])
        elif component_type == "checkbox":
            return Checkbox(
                checked=field_config.default if isinstance(field_config.default, bool) else False,
                **common_kwargs
            )
        # Add more component types as needed
        else:
            raise ValueError(f"Unsupported form component type: {component_type}")

    def generate_form(self, form_id: str = "dynamic-form") -> Page:
        form_title = self.config.form_title or f"Create {self.config.resource_name}"
        
        form_component = Form(
            id=form_id,
            action=f"{self.config.api_prefix or f'/api/{self.config.table_name or self.config.resource_name.lower() + 's'}'}",
            method="post",
            add_class_name=self.config.form_layout_class
        )
        
        form_component.add_child(Heading(level=2, content=form_title))
        
        for field in self.config.fields:
            if not field.primary_key and not field.hidden: # Primary key and hidden fields are not in the form
                field_form_component = self._get_form_component(field)
                if field_form_component:
                    form_component.add_child(Div(components=[field_form_component], add_class_name="mb-4"))
        
        # Add submit and cancel buttons
        buttons_div = Div(add_class_name="flex justify-end space-x-2")
        buttons_div.add_child(Button(
            type="button",
            content=self.config.form_cancel_button_text,
            add_class_name=self.config.form_cancel_button_class,
            on_click="window.history.back()"
        ))
        buttons_div.add_child(Button(
            type="submit",
            content=self.config.form_submit_button_text,
            add_class_name=self.config.form_submit_button_class
        ))
        form_component.add_child(buttons_div)
        
        if self.config.extra_form_components:
            for extra_comp_data in self.config.extra_form_components:
                # Assuming extra_comp_data is already a valid component dict for backend.components
                # For now, we'll just add it raw, more sophisticated parsing can be added if needed
                # A better approach would be to have a helper function to build components from dict
                pass # This requires a recursive component builder for frontend components from dict
        
        return Page(label=form_title, components=[form_component])

# --- Dynamic CRUD Manager ---
class DynamicCRUDManager:
    def __init__(self, app: FastAPI):
        self.app = app
        self.resources: Dict[str, Any] = {} # Stores models, schemas, routers, etc.

    def register_resource(self, config: DynamicCRUDConfig):
        # 1. Generate SQLModel
        sql_model = generate_sqlmodel(config)
        # For SQLModel, tables are created via SQLModel.metadata.create_all
        # This should be called once on startup

        # 2. Generate Pydantic Schemas
        schemas = generate_pydantic_schemas(config, sql_model)
        
        # 3. Generate FastAPI Router
        router_kwargs = config.router_kwargs.copy()
        router_kwargs.pop('prefix', None)  # Remove prefix from kwargs to avoid conflict
        
        router = APIRouter(
            prefix=config.api_prefix or f"/api/{config.table_name or config.resource_name.lower() + 's'}",
            tags=[config.resource_name],
            **router_kwargs
        )

        db_dependency = Depends(config.db_session_dependency)
        
        # Primary key field name and type
        pk_field_config = next((f for f in config.fields if f.primary_key), None)
        if not pk_field_config:
            raise ValueError(f"Resource '{config.resource_name}' must have a primary key defined.")
        
        pk_field_name = pk_field_config.name
        pk_py_type = PYTHON_TYPE_MAP.get(pk_field_config.type)
        if pk_py_type is None:
            raise ValueError(f"Primary key field '{pk_field_name}' has an unknown Python type: {pk_field_config.type}")

        # 4. Register API Endpoints
        
        # Create
        @router.post("/", response_model=schemas["Base"])
        def create_item(item: Type[BaseModel], db: Session = db_dependency):
            # Ensure item is converted to the correct SQLModel type for validation
            db_item = sql_model.model_validate(item) # Use model_validate for SQLModel
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item

        # Read All
        @router.get("/", response_model=List[schemas["Base"]])
        def read_all_items(skip: int = 0, limit: int = 100, db: Session = db_dependency):
            items = db.exec(select(sql_model).offset(skip).limit(limit)).all()
            return items

        # Read One
        @router.get(f"/{{'{pk_field_name}':{pk_py_type.__name__}}}", response_model=schemas["Base"])
        def read_item(item_id: pk_py_type, db: Session = db_dependency):
            db_item = db.exec(select(sql_model).where(getattr(sql_model, pk_field_name) == item_id)).first()
            if db_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{config.resource_name} not found")
            return db_item

        # Update
        @router.put(f"/{{'{pk_field_name}':{pk_py_type.__name__}}}", response_model=schemas["Base"])
        def update_item(item_id: pk_py_type, item: Type[BaseModel], db: Session = db_dependency):
            db_item = db.exec(select(sql_model).where(getattr(sql_model, pk_field_name) == item_id)).first()
            if db_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{config.resource_name} not found")
            
            for key, value in item.dict(exclude_unset=True).items():
                setattr(db_item, key, value)
            
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item

        # Delete
        @router.delete(f"/{{'{pk_field_name}':{pk_py_type.__name__}}}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_item(item_id: pk_py_type, db: Session = db_dependency):
            db_item = db.exec(select(sql_model).where(getattr(sql_model, pk_field_name) == item_id)).first()
            if db_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{config.resource_name} not found")
            
            db.delete(db_item)
            db.commit()
            return None # 204 No Content

        self.app.include_router(router)
        
        # 5. Generate and register Form endpoint
        form_generator = DynamicFormGenerator(config)
        
        @router.get("/form", response_model=Dict[str, Any], include_in_schema=False)
        def get_resource_form():
            return form_generator.generate_form().to_dict()

        self.resources[config.resource_name] = {
            "model": sql_model,
            "schemas": schemas,
            "router": router,
            "config": config,
            "form_generator": form_generator,
        }
        
    def get_resource(self, resource_name: str):
        if resource_name not in self.resources:
            raise ValueError(f"Resource '{resource_name}' not registered.")
        return self.resources[resource_name]
