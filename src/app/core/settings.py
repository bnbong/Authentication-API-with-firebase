# --------------------------------------------------------------------------
# Backend Application의 설정을 관리하는 파일입니다.
#
# .env 파일을 통해 설정을 관리합니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    SECRET_KEY: str = Field(
        default="HhingmORugetCchi?",
        description="Secret key for JWT.",
    )
    JWT_ALGORITHM: str = Field(
        default="AHNARLLYAJUM2048",
        description="Algorithm for JWT.",
    )
    LOGGING_LEVEL: bool = Field(
        default=False,
        description="True: DEBUG mode, False:: INFO mode",
    )

    model_config = SettingsConfigDict(env_file=".env.settings")
