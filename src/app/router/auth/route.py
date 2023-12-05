import os
import json
import secrets
import logging
import base64

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse

import google_auth_oauthlib.flow

from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from firebase_admin.auth import UserNotFoundError
from binascii import Error as binasciiError

from app.crud.token import get_firebase_id_token_with_email

from dotenv import load_dotenv

# from app.schemas.auth import VerifyTokenResponse
# from app.router.auth.verify import verify_token
# from app.crud.token import findByToken, delToken, createToken
# from app.utils.log import logger
# from app.db.redis import get_redis

load_dotenv()
logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth")


# --------------------------------------------------------------------------
# Google OAuth 로그인 및 Firebase ID 토큰 발급
# --------------------------------------------------------------------------
@auth_router.get(
    "/login",
    summary="Google OAuth 로그인",
    description="Google OAuth 로그인을 수행합니다. 로그인이 완료되면 /api/v1/auth/auth url로 리다이렉션됩니다.",
)
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
    google_key_path = os.path.join(
        os.path.dirname(__file__), "../../../", os.getenv("GOOGLE_CLIENT_KEY")
    )
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        google_key_path, scopes=scopes
    )
    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    flow.fetch_token(code=code)

    credentials = flow.credentials
    return credentials.id_token


@auth_router.get(
    "/auth",
    summary="Google 로그인 정보를 바탕으로 Firebase ID 토큰 발급",
    description="Google OAuth 로그인을 수행하면, Firebase ID 토큰을 발급받습니다.",
)
async def auth(request: Request):
    # URL 쿼리 파라미터에서 인증 코드 추출
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    # Google 사용자 인증 정보 얻기
    try:
        id_token = await get_google_user_info(code)
        decoded_token = base64.urlsafe_b64decode(
            id_token.split(".")[1] + "=" * (-len(id_token) % 4)
        )
        user_email = json.loads(decoded_token.decode("utf-8")).get("email")

        uid, firebase_id_token = await get_firebase_id_token_with_email(user_email)

        logger.info(f"Firebase user logged in: UID={uid}, Email={user_email}")

        return JSONResponse(
            {"user_email": user_email, "firebase_id_token": firebase_id_token}
        )

    except InvalidGrantError as exc:
        logger.info(
            "Validating Google user information via provided OAuth authorization code is failed"
        )
        return JSONResponse(
            {"error": "잘못된 유저 정보를 전송했습니다.", "detail": str(exc)}, status_code=400
        )

    except UserNotFoundError as exc:
        logger.info(f"Firebase user not found: {str(exc)}")
        return JSONResponse(
            {"error": "자람 그룹웨어 Firebase에 등록되지 않은 유저입니다.", "detail": str(exc)},
            status_code=404,
        )

    except binasciiError as exc:
        logger.info(f"Failed to decode given Google ID token: {id_token}")
        return JSONResponse(
            {
                "error": "Google Id token을 decoding 하는 과정에 문제가 발생했습니다.",
                "detail": str(exc),
            },
            status_code=500,
        )


# --------------------------------------------------------------------------
# Firebase ID 토큰 검증 및 캐싱 (Redis를 활용하는 로직, 현재 버전에서는 사용X)
# --------------------------------------------------------------------------
# @auth_router.get("/verify/{firebase_token}", response_model=VerifyTokenResponse)
# async def authorization(firebase_token: str, rd=Depends(get_redis)):
#     cache_check = findByToken(firebase_token, rd)
#
#     if cache_check is True:
#         return {"verify": True}
#
#     else:
#         verify_result = verify_token(firebase_token)
#
#         if verify_result is None:
#             return {"verify": False}
#
#         else:
#             uid, exp = verify_result
#
#             await createToken(firebase_token, int(exp), uid, rd)
#
#             return {"verify": True}
#
#
# @auth_router.delete("/revoke/{firebase_token}")
# async def revoke_token(firebase_token: str, rd=Depends(get_redis)):
#     check = await delToken(firebase_token, rd)
#     if check is True:
#         logger.info(f"// app.router.auth.route // token {firebase_token} is revoked")
#         return {"token": firebase_token}
#
#     else:
#         return HTTPException(417)
