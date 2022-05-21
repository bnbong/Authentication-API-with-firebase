from fastapi import APIRouter,HTTPException,Depends
from app.msng.app.schemas.auth import verifyTokenResponse,delTokenResponse
from app.msng.app.api.api_v1.endpoints.auth.verify import verify_token
from app.msng.app.crud.token import findByToken,delToken,createToken
from app.msng.app.utils.log import logger
from app.msng.app.db.redis import get_redis
auth_router = APIRouter(prefix="/auth")


@auth_router.get("/verify/{firebase_token}",response_model=verifyTokenResponse)
async def authorization(firebase_token: str,rd = Depends(get_redis)):

    cache_check = findByToken(firebase_token,rd)

    if cache_check is True:
        return {"verify": True}

    else:
        verify_result = verify_token(firebase_token)

        if verify_result is None:

            return {"verify": False}

        else:
            uid, exp = verify_result

            await createToken(firebase_token,int(exp),uid,rd)

            return {"verify": True}


@auth_router.delete("/revoke/{firebase_token}")
async def revoke_token(firebase_token: str,rd = Depends(get_redis)):

    check = await delToken(firebase_token,rd)
    if check is True:
        logger.info(f"// app.msng.app.api.api_v1.endpoints.auth.route // token {firebase_token} is revoked")
        return {"token" : firebase_token}

    else:
        return HTTPException(417)