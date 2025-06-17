from middlewares.linebot.linebot_base_handler import LineBotBaseHandler
from linebot.models import MessageEvent, TextMessage
from middlewares.webhook.text_units.account_exec_unit import AccountExecUnit


class TextMessageHandler(LineBotBaseHandler):
    def __init__(self, line_bot_api, line_bot_handler):
        super().__init__(line_bot_api, line_bot_handler)

    def register(self):
        @self._handler.add(MessageEvent, message=TextMessage)
        def handle(event):
            text = event.message.text
            if text.lower().startswith('account'):
                exec_unit = AccountExecUnit(text)
                exec_unit.exec()
