import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from app.crud.token import generate_tokens

logger = logging.getLogger(__name__)

hub_router = APIRouter(prefix="/hub/token")


@hub_router.post(
    "/",
    summary="Google 로그인을 통해 발급받은 Firebase ID token을 이용하여 access token, refresh token 발급",
    description="클라이언트에서 Google OAuth2.0 로그인을 수행하면 Google OAuth2.0 인증 서버에서 발급받은 인증 코드를 이용하여 \
    Firebase ID token을 발급받습니다(/api/v1/auth/auth endpoint에서). 이 Firebase ID token을 이용하여 access token, refresh token을 발급받습니다. 만약, \
    redirect_uri가 제공된 경우, 해당 URL로 서버가 자동으로 redirect합니다.",
)
async def hub_issue_access_token_with_firebase_idtoken(
    user_email: str, firebase_id_token: str, redirect_uri: str = None
):
    if not firebase_id_token:
        raise HTTPException(status_code=400, detail="Firebase ID token is missing")

    access_token, refresh_token = generate_tokens(user_email=user_email, firebase_id_token=firebase_id_token)

    if redirect_uri:
        # redirect_uri가 제공된 경우, RedirectResponse 객체를 생성하고 여기에 쿠키를 추가
        response = RedirectResponse(url=redirect_uri)
    else:
        # redirect_uri가 없는 경우, 일반 JSONResponse 객체를 사용
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
async def hub_refresh_access_token():
    pass


@hub_router.post(
    "/revoke",
    summary="access token, refresh token을 폐기.",
    description="클라이언트에서 로그아웃을 수행하면 access token, refresh token을 폐기합니다.",
)
async def hub_revoke_tokens():
    pass


@hub_router.get(
    "/verify",
    summary="access token을 검증.",
    description="access token을 검증하여 access token으로부터 firebase id token을 추출합니다.",
)
async def hub_verify_tokens():
    pass
