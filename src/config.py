import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)

    DEBUG: bool = False

    # ---Config--- #
    # 系統名稱
    SYSTEM_NAME: str
    # 產品名稱
    APP_NAME: str
    # 產品版本
    APP_VERSION: str
    # 產品環境
    STAGE: str

    # ---Service--- #

    # LineBotAPI
    LINEBOT_SECRET: str
    LINEBOT_ACCESS_TOKEN: str

    # Google Sheet
    GOOGLE_CLIENT_SECRET_FILE_PATH: str
    GOOGLE_SHEET_URL: str

    # ---Postgresql--- #
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_USER_PASS: str
    DB_NAME: str

    # ---Redis--- #
    REDIS_HOST: str
    REDIS_PORT: int
    ACCOUNT_DB_NUM: int
    USER_DB_NUM: int
    ACCOUNT_EXPIRED_TIME: int = 60 * 5
    USER_CREATE_EXPIRED_TIME: int = 60 * 5


class Testing(Settings):
    TESTING: bool = True
    DEBUG: bool = True


def get_setting():
    stage = os.getenv("STAGE")
    if stage == "dev":
        return Testing()
    return Settings()


Config = get_setting()
