from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from app.router import api_v1_route
from app.db.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Application startup")
        print("Create connection and setting up database")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        print("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_route)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=18000)
