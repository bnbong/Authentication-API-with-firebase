from app.db.redis import get_redis
from app.utils.log import logger


async def findByToken(token: str, redis) -> bool:
    try:
        async with redis.client() as conn:
            val = await conn.get(token)

        logger.debug(f"{val} // app.router.auth.lookaside.check_cahce")
        assert val is not None

    except Exception as e:
        logger.error(f"{e} // app.router.auth.lookaside.check_cahce // raise error")
        return False

    return True


async def createToken(token, exp: int, uid: str, redis) -> bool:
    try:
        async with redis.client() as conn:
            await conn.set(token, uid)
            await conn.expire(token, exp)

    except Exception as e:
        logger.error(f"{e} // app.router.auth.lookaside.add_cache // raise error")

        return False

    logger.debug(
        f"// app.router.auth.lookaside.add_cache // {token} is successfully add to redis! by {exp} sec."
    )
    return True


async def delToken(token: str, redis) -> bool:
    try:
        async with redis.client() as conn:
            await conn.delete(token)

    except Exception as e:
        logger.error(f"{e} // app.router.auth.lookaside.del_cache // raise error")

        return False

    logger.debug(
        f"// app.router.auth.lookaside.del_cache // {token} is successfully del to redis!"
    )
    return True
