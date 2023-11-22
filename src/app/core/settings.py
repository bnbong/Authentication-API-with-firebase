# --------------------------------------------------------------------------
# Backend Application의 설정을 관리하는 파일입니다.
#
# .env 파일을 통해 설정을 관리합니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    DATABASE_URI: AnyUrl = Field(
        default="mysql+aiomysql://bnbong:password@localhost:3307/auth-db",
        description="MariaDB connection URI.",
    )
    DATABASE_OPTIONS: Dict[str, Any] = Field(
        default={
            "pool_size": 10,
            "max_overflow": 20,
            "pool_recycle": 300,
            "pool_pre_ping": True,
        },
        description="MariaDB option to create a connection.",
    )
    LOGGING_LEVEL: bool = Field(
        default=False,
        description="True: DEBUG mode, False:: INFO mode",
    )

    class ConfigDict:
        env_file = ".env"
