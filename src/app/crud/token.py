# from app.db.redis import get_redis
# from app.utils.log import logger
#
#
# async def findByToken(token: str, redis) -> bool:
#     try:
#         async with redis.client() as conn:
#             val = await conn.get(token)
#
#         logger.debug(f"{val} // app.router.auth.lookaside.check_cahce")
#         assert val is not None
#
#     except Exception as e:
#         logger.error(f"{e} // app.router.auth.lookaside.check_cahce // raise error")
#         return False
#
#     return True
#
#
# async def createToken(token, exp: int, uid: str, redis) -> bool:
#     try:
#         async with redis.client() as conn:
#             await conn.set(token, uid)
#             await conn.expire(token, exp)
#
#     except Exception as e:
#         logger.error(f"{e} // app.router.auth.lookaside.add_cache // raise error")
#
#         return False
#
#     logger.debug(
#         f"// app.router.auth.lookaside.add_cache // {token} is successfully add to redis! by {exp} sec."
#     )
#     return True
#
#
# async def delToken(token: str, redis) -> bool:
#     try:
#         async with redis.client() as conn:
#             await conn.delete(token)
#
#     except Exception as e:
#         logger.error(f"{e} // app.router.auth.lookaside.del_cache // raise error")
#
#         return False
#
#     logger.debug(
#         f"// app.router.auth.lookaside.del_cache // {token} is successfully del to redis!"
#     )
#     return True
import os
import jwt
import requests
import datetime

from typing import Tuple
from jwt import PyJWTError

from fastapi import HTTPException

from firebase_admin import auth as firebase_auth

from app.core.settings import AppSettings

app_settings = AppSettings()


def create_firebase_custom_token(uid: str):
    firebase_auth.get_user(uid)
    firebase_custom_token = firebase_auth.create_custom_token(uid)
    return firebase_custom_token


async def get_firebase_id_token(firebase_custom_token: bytes):
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    request_data = {"token": firebase_custom_token, "returnSecureToken": True}
    response = requests.post(
        f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={firebase_api_key}",
        data=request_data,
    )
    response_data = response.json()
    return response_data.get("idToken")


async def get_firebase_id_token_with_email(user_email: str) -> Tuple[str, str]:
    # Firebase 커스텀 토큰 생성
    firebase_user = firebase_auth.get_user_by_email(user_email)
    uid = firebase_user.uid
    firebase_custom_token = create_firebase_custom_token(uid)

    # Firebase ID 토큰 반환
    firebase_id_token = await get_firebase_id_token(firebase_custom_token)
    if not firebase_id_token:
        raise HTTPException(
            status_code=500, detail="Failed to exchange custom token"
        )

    return uid, firebase_id_token


def generate_tokens(user_email: str, firebase_id_token: str) -> Tuple[str, str]:
    now = datetime.datetime.utcnow()

    # Access Token 페이로드에 Firebase ID 토큰 정보 포함
    access_token_payload = {
        "sub": user_email,
        "firebase_id_token": firebase_id_token,
        "iat": now,
        "exp": now + datetime.timedelta(hours=1),
    }
    access_token = jwt.encode(
        access_token_payload,
        app_settings.SECRET_KEY,
        algorithm=app_settings.JWT_ALGORITHM,
    )

    refresh_token_payload = {
        "sub": user_email,
        "iat": now,
        "exp": now + datetime.timedelta(days=7),
    }
    refresh_token = jwt.encode(
        refresh_token_payload,
        app_settings.SECRET_KEY,
        algorithm=app_settings.JWT_ALGORITHM,
    )

    return access_token, refresh_token


def verify_refresh_token(refresh_token: str) -> str:
    try:
        decoded_token = jwt.decode(
            refresh_token,
            app_settings.SECRET_KEY,
            algorithms=[app_settings.JWT_ALGORITHM]
        )
        # 추출된 이메일 반환
        email = decoded_token.get("sub")
        print(email)
        return email
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def verify_access_token(access_token: str) -> str:
    try:
        decoded_token = jwt.decode(
            access_token,
            app_settings.SECRET_KEY,
            algorithms=[app_settings.JWT_ALGORITHM]
        )
        # 추출된 Firebase ID 토큰 반환
        return decoded_token.get("firebase_id_token")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
