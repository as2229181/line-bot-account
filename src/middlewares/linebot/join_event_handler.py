from linebot.models import CarouselColumn, CarouselTemplate, JoinEvent, MessageAction, TemplateSendMessage

from middlewares.linebot.linebot_base_handler import LineBotBaseHandler


class JoinEventHandler(LineBotBaseHandler):
    def __init__(self, line_bot_api, line_bot_handler):
        super().__init__(line_bot_api, line_bot_handler)

    def register(self):
        @self._handler.add(JoinEvent)
        def handle(event):
            message = TemplateSendMessage(
                alt_text='歡迎加入草莓成福\n請先確認使用者狀態！',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title='確認使用者狀態',
                            text='user',
                            actions=[MessageAction(label='查看使用者狀態', text='user')],
                        ),
                    ],
                ),
            )
            self._api.reply_message(event.reply_token, message)
