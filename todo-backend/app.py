from fastapi import FastAPI
from api import router as app_router
from database import create_tables

app = FastAPI()

# Initialize the database
create_tables()

app.include_router(app_router, prefix="", tags=[""])
