from contextlib import asynccontextmanager

import os
import firebase_admin
import uvicorn

from fastapi import FastAPI

from app.router import api_v1_route
from app.utils.log import logger
from app.utils.exceptions import CustomExceptionMiddleware

# from app.db.database import engine, Base


from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Application startup...")  # print 대신 logger 사용
        logger.info("Firebase admin initializing...")
        firebase_key_path = os.path.join(
            os.path.dirname(__file__), os.getenv("FIRE_BASE_KEY")
        )
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase admin setup complete")
        # print("Create connection and setting up database")
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)
        #     print("DB connection created")
        yield
    finally:
        logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_route)
app.add_middleware(CustomExceptionMiddleware)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=18000)
