import os

from fastapi import FastAPI
from src.database import create_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = os.environ["DB_CONNECTION_STRING"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.post("/host/create_data")
async def create_data():
    create_db()
    return {"Status": "OK"}


@app.get("/health")
async def health_check():
    return {"Status": "OK"}


@app.on_event("startup")
async def on_startup():
    create_db()
    app.state.db = SessionLocal()


@app.on_event("shutdown")
async def shutdown():
    app.state.db.close()
