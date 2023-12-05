import logging

from fastapi import APIRouter, HTTPException, Request, Response, Header
from fastapi.responses import JSONResponse

from firebase_admin import auth as firebase_auth

from app.crud.token import generate_tokens, verify_refresh_token, verify_access_token, get_firebase_id_token_with_email

logger = logging.getLogger(__name__)

hub_router = APIRouter(prefix="/hub/token")


# --------------------------------------------------------------------------
# 자람 허브 토큰 endpoint
# --------------------------------------------------------------------------
@hub_router.post(
    "/",
    summary="Google 로그인을 통해 발급받은 Firebase ID token을 이용하여 access token, refresh token 발급",
    description="클라이언트에서 Google OAuth2.0 로그인을 수행하면 Google OAuth2.0 인증 서버에서 발급받은 인증 코드를 이용하여 \
    Firebase ID token을 발급받습니다(/api/v1/auth/auth endpoint에서). 이 Firebase ID token을 이용하여 access token, refresh token을 발급받습니다.\
    이때, access_token은 변수로 리턴되며(클라이언트에서 access_token을 별도의 변수로 관리), refresh_token은 HTTP 쿠키로 관리됩니다.",
)
async def hub_issue_access_token_with_firebase_idtoken(
    user_email: str, firebase_id_token: str
):
    if not firebase_id_token:
        raise HTTPException(status_code=400, detail="Firebase ID token is missing")

    try:  # firebase_id_token이 유효한지 검증
        firebase_auth.verify_id_token(firebase_id_token)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail=str(e))

    access_token, refresh_token = generate_tokens(
        user_email=user_email, firebase_id_token=firebase_id_token
    )

    response = JSONResponse({"access_token": access_token})

    # Refresh Token을 HTTP 쿠키에 저장
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # JavaScript로부터 보호 (XSS 방지)
        secure=False,  # HTTP, HTTPS 둘다 전송 가능 (TODO: 추후 배포 시 True로 변경)
        max_age=3600 * 24 * 7,  # 유효 기간: 7일
    )

    return response


@hub_router.post(
    "/refresh",
    summary="Refresh token을 이용하여 새로 access token 발급",
    description="Refresh token의 정보를 이용하여 새로 access token을 (firebase id token과 같이) 발급합니다.",
)
async def hub_refresh_access_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    user_email = verify_refresh_token(refresh_token)

    _, new_firebase_id_token = await get_firebase_id_token_with_email(user_email=user_email)
    access_token, new_refresh_token = generate_tokens(user_email=user_email, firebase_id_token=new_firebase_id_token)

    response = JSONResponse({"access_token": access_token})

    # Refresh Token을 HTTP 쿠키에 저장
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  # (TODO: 추후 배포 시 True로 변경)
        max_age=3600 * 24 * 7,
    )

    return response


@hub_router.post(
    "/revoke",
    summary="access token, refresh token을 폐기.",
    description="클라이언트에서 로그아웃을 수행하면 cookie에 있는 refresh token을 폐기합니다. (access_token은 변수로 관리되니 제외)",
)
async def hub_revoke_tokens(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Refresh token revoked successfully"}


@hub_router.get(
    "/verify",
    summary="access token을 검증.",
    description="access token을 검증하여 access token으로부터 firebase id token을 추출합니다.",
)
async def hub_verify_tokens(access_token: str = Header(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")

    firebase_id_token = verify_access_token(access_token)

    return JSONResponse({"firebase_id_token": firebase_id_token})
