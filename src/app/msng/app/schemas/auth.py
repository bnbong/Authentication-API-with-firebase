from app.msng.app.schemas.orm import OrmBaseModel
from typing import Optional


class verifyTokenResponse(OrmBaseModel):

    verify: bool

class delTokenResponse(OrmBaseModel):

    token: str