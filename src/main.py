from contextlib import asynccontextmanager

import os
import firebase_admin
import uvicorn

from fastapi import FastAPI

from app.router import api_v1_route
from app.db.database import engine, Base


from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Application startup...")
        print("Firebase admin initializing...")
        cred = credentials.Certificate(os.getenv("FIRE_BASE_KEY"))
        firebase_admin.initialize_app(cred)
        print("Firebase admin setup complete")
        print("Create connection and setting up database")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("DB connection created")
        yield
    finally:
        print("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_route)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=18000)
