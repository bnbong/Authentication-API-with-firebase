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

import jwt
import datetime

from typing import Tuple

from app.core.settings import AppSettings

app_settings = AppSettings()


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
        access_token_payload, app_settings.SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM
    )

    refresh_token_payload = {
        "sub": user_email,
        "iat": now,
        "exp": now + datetime.timedelta(days=7),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, app_settings.SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM
    )

    return access_token, refresh_token
