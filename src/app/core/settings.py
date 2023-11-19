# --------------------------------------------------------------------------
# Backend Application의 설정을 관리하는 파일입니다.
#
# 실제 환경에서는 .env 파일을 통해 설정을 관리하며,
# 테스트 환경에서는 .env.test 파일을 통해 설정을 관리합니다.
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

    class ConfigDict:
        env_file = ".env"
