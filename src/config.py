import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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
    # 服務器密鑰
    APP_SECRET: str

    # ---Service--- #

    # LineBotAPI
    LINEBOT_SECRET: str
    LINEBOT_ACCESS_TOKEN: str

    # Google Sheet
    GOOGLE_AUTHORIZE_TOKEN: str
    GOOGLE_SHEET_URL_ROOT: str
    GOOGLE_SHEET_ID: str


class Testing(Settings):
    TESTING: bool = True
    DEBUG: bool = True


def get_setting():
    stage = os.getenv("STAGE")
    if stage == "dev":
        return Testing
    return Settings


Config = get_setting()
