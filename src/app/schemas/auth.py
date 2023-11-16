from typing import Optional

from app.schemas.orm import OrmBaseModel


class VerifyTokenResponse(OrmBaseModel):
    verify: bool


class DelTokenResponse(OrmBaseModel):
    token: str
