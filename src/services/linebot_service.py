from consts.linebot_const import MessageType
from linebot import LineBotApi, WebhookHandler
from middlewares.linebot.text_message_handler import TextMessageHandler


class LineBotService:
    _VALID_MESSAGE_TYPE = {MessageType.TEXT}

    def __init__(self, access_token, secret):
        self._line_bot_api = LineBotApi(access_token)
        self._handler = WebhookHandler(secret)
        self._register_handler()

    def _register_handler(self):
        handlers = [TextMessageHandler(self._line_bot_api, self._handler)]
        for handler in handlers:
            handler.register()

    def validate(self, body, signature):
        self._handler.handle(body, signature)
        return True
