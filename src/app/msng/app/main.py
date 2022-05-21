from fastapi import FastAPI
import uvicorn
from app.msng.app.api.api_v1.route import api_v1_route


app = FastAPI()

app.include_router(api_v1_route)


if __name__ == "__main__":

    uvicorn.run(app, host='127.0.0.1', port=18000)

