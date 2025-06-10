from linebot import LineBotApi, WebhookHandler
from consts.linebot_const import MessageType


class LineBotService:
    _VALID_MESSAGE_TYPE = {MessageType.TEXT}

    def __init__(self, access_token, secret):
        self._linebot_api = LineBotApi(access_token)
        self._handler = WebhookHandler(secret)

    @property
    def handler(self):
        return self._handler

    def validate(self, body, signature):
        self._handler.handle(body, signature)
        return True
