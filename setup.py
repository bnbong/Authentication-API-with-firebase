# --------------------------------------------------------------------------
# Backend Application의 패키지 정보를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from setuptools import setup, find_packages

install_requires = [
    # Main Application Dependencies
    "fastapi==0.104.0",
    "uvicorn==0.24.0.post1",
    # ORM Dependencies
    "alembic==1.12.1",
    "SQLAlchemy==2.0.23",
    "pydantic==2.5.1",
    "pydantic_core==2.14.3",
    "pydantic-settings==2.1.0",
    "alembic==1.12.0",
    "aioredis==2.0.1",
    "aiomysql==0.2.0",
    "greenlet==3.0.1",
    # Utility Dependencies
    "python-dotenv==1.0.0",
    "pytest==7.4.3",
    "firebase-admin==6.2.0",
    "python-dotenv==1.0.0",
]

# IDE will watch this setup config through your project src, and help you to set up your environment
setup(
    name="authentication-firebase-api",
    description="Firebase SDK를 이용한 user token 인증 application",
    author="bnbong",
    author_email="bbbong9@gmail.com",
    packages=find_packages(where="app"),
    use_scm_version=True,
    requires=["python (>=3.10)"],
    install_requires=install_requires,
)
