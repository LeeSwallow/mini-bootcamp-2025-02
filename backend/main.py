import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.documents import router as documents_router

from app.dependencies.db import create_db_and_tables, drop_db_and_tables
from app.dependencies.oauth2 import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    # On Startup Event
    # drop_db_and_tables()
    create_db_and_tables()
    
    load_dotenv()
    
    yield
    # On Shutdown Event

app = FastAPI(lifespan=lifespan_manager)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(documents_router)
    