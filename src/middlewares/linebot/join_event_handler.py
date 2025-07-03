from linebot.models import JoinEvent, TextSendMessage

from middlewares.linebot.linebot_base_handler import LineBotBaseHandler


class JoinEventHandler(LineBotBaseHandler):
    def __init__(self, line_bot_api, line_bot_handler):
        super().__init__(line_bot_api, line_bot_handler)

    def register(self):
        @self._handler.add(JoinEvent)
        def handle(event):
            message = TextSendMessage(text='歡迎加入\n請輸入 「user-create」\n已新增使用者\n或者輸入 「help 查詢指令」！')
            self._api.reply_message(event.reply_token, message)
