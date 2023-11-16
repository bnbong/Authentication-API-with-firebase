import os
import requests

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer

from dotenv import load_dotenv

from app.schemas.auth import VerifyTokenResponse, DelTokenResponse
from app.router.auth.verify import verify_token
from app.crud.token import findByToken, delToken, createToken
from app.utils.log import logger
from app.db.redis import get_redis

load_dotenv()

auth_router = APIRouter(prefix="/auth")


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    refreshUrl="https://oauth2.googleapis.com/token",
    scopes={"openid": "OpenID Connect scope"},
)


@auth_router.get("/login")
def login():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    scope = "https://www.googleapis.com/auth/userinfo.email"
    response_type = "code"

    return RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/auth?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


@auth_router.get("/auth")
def auth(code: str = Depends(oauth2_scheme)):
    # Google로부터 인증 코드를 받아 ID 토큰으로 교환
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }
    response = requests.post(oauth2_scheme.tokenUrl, data=data)
    response_data = response.json()

    if "id_token" not in response_data:
        raise HTTPException(status_code=400, detail="Google ID Token not found")

    # Firebase Admin을 사용하여 ID 토큰 검증
    decoded_token = auth.verify_id_token(response_data["id_token"])
    return {"user_id_token": decoded_token["uid"]}


@auth_router.get("/verify/{firebase_token}", response_model=VerifyTokenResponse)
async def authorization(firebase_token: str, rd=Depends(get_redis)):
    cache_check = findByToken(firebase_token, rd)

    if cache_check is True:
        return {"verify": True}

    else:
        verify_result = verify_token(firebase_token)

        if verify_result is None:
            return {"verify": False}

        else:
            uid, exp = verify_result

            await createToken(firebase_token, int(exp), uid, rd)

            return {"verify": True}


@auth_router.delete("/revoke/{firebase_token}")
async def revoke_token(firebase_token: str, rd=Depends(get_redis)):
    check = await delToken(firebase_token, rd)
    if check is True:
        logger.info(f"// app.router.auth.route // token {firebase_token} is revoked")
        return {"token": firebase_token}

    else:
        return HTTPException(417)
