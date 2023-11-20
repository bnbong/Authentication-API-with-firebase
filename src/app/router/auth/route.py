import os
import json
import secrets
import requests
import base64

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

from firebase_admin import auth as firebase_auth
import google_auth_oauthlib.flow

from dotenv import load_dotenv

from app.schemas.auth import VerifyTokenResponse
from app.router.auth.verify import verify_token
from app.crud.token import findByToken, delToken, createToken
from app.utils.log import logger
from app.db.redis import get_redis

load_dotenv()

auth_router = APIRouter(prefix="/auth")


# --------------------------------------------------------------------------
# Google OAuth 로그인 및 Firebase ID 토큰 발급
# --------------------------------------------------------------------------
@auth_router.get("/login")
def login():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    scope = "https://www.googleapis.com/auth/userinfo.email"
    response_type = "code"
    state = secrets.token_urlsafe()

    return RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/auth?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
    )


async def get_google_user_info(code: str):
    scopes = ["openid", "https://www.googleapis.com/auth/userinfo.email"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.getenv("GOOGLE_CLIENT_KEY"), scopes=scopes)
    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    flow.fetch_token(code=code)

    credentials = flow.credentials
    return credentials.id_token


def create_firebase_custom_token(uid: str):
    firebase_auth.get_user(uid)
    firebase_custom_token = firebase_auth.create_custom_token(uid)
    return firebase_custom_token


async def get_firebase_id_token(firebase_custom_token: bytes):
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    request_data = {
        "token": firebase_custom_token,
        "returnSecureToken": True
    }
    response = requests.post(
        f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={firebase_api_key}",
        data=request_data
    )
    response_data = response.json()
    return response_data.get("idToken")


@auth_router.get("/auth")
async def auth(request: Request):
    # URL 쿼리 파라미터에서 인증 코드 추출
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    # Google 사용자 인증 정보 얻기
    id_token = await get_google_user_info(code)

    decoded_token = base64.urlsafe_b64decode(id_token.split('.')[1] + '=' * (-len(id_token) % 4))
    user_email = json.loads(decoded_token.decode('utf-8')).get('email')

    # Firebase 커스텀 토큰 생성
    firebase_user = firebase_auth.get_user_by_email(user_email)
    uid = firebase_user.uid
    firebase_custom_token = create_firebase_custom_token(uid)

    # Firebase ID 토큰 반환
    firebase_id_token = await get_firebase_id_token(firebase_custom_token)
    if not firebase_id_token:
        raise HTTPException(status_code=500, detail="Failed to exchange custom token")

    return {"firebase_id_token": firebase_id_token}


# --------------------------------------------------------------------------
# Firebase ID 토큰 검증 및 캐싱
# --------------------------------------------------------------------------
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
