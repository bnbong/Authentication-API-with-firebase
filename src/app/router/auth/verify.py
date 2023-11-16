from firebase_admin.auth import (
    verify_id_token,
    ExpiredIdTokenError,
    InvalidIdTokenError,
)

from app.utils.log import logger


def verify_token(token: str) -> tuple:
    try:
        decode_token = verify_id_token(token)

    except ExpiredIdTokenError:
        logger.warning(
            f"ExpiredIdTokenError // app.router.auth.verify //  ID token ( {token} ) has expired."
        )
        return None, None

    except InvalidIdTokenError:
        logger.warning(
            f"InvalidIdTokenError // app.router.auth.verify //  ID token ( {token} ) is not a valid Firebase ID token."
        )
        return None, None

    except ValueError:
        logger.error(
            f"ValueError // app.router.auth.verify // id_token is a not a string or is empty. "
        )
        return None, None

    except Exception as e:
        logger.error(f"{e} // app.router.auth.verify // raise up some Error")
        return None, None

    if decode_token is None:
        logger.error(f"ValueError // app.router.auth.verify // decode token is None ")
        raise ValueError

    else:
        try:
            uid = decode_token["uid"]
            exp = decode_token["exp"]

        except Exception as e:
            logger.error(
                f"{e} // app.router.auth.verify // ID token ( {token} )'s decode token doesn't have aud or exp"
            )
            return None, None

        return uid, exp
