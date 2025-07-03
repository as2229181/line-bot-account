from linebot.models import MessageEvent, TextMessage, TextSendMessage

from middlewares.linebot.linebot_base_handler import LineBotBaseHandler
from middlewares.webhook.text_units.text_dispatcher import TextDispatcher


class TextMessageHandler(LineBotBaseHandler):
    def __init__(self, line_bot_api, line_bot_handler):
        super().__init__(line_bot_api, line_bot_handler)

    @staticmethod
    def _extract_text_to_list(message) -> list:
        """
        split text message
        'account' => ['account']
        'account-delete' => ['account', 'delete']
        """
        raw_text = message.get('text', '').strip()
        if ' ' in raw_text:
            command, args = raw_text.split(' ', 1)
            parts = command.split('-') + [args]
        else:
            parts = raw_text.split('-')

        return parts

    def register(self):
        @self._handler.add(MessageEvent, message=TextMessage)
        def handle(event):
            text = event.message.text
            user_uuid = event.source.user_id
            exec_unit = TextDispatcher.dispatch(text, user_uuid)
            if exec_unit is None:
                self._api.reply_message(event.reply_token, TextSendMessage(text='❌ 請確認指令是否正確。'))
                return
            try:
                reply = exec_unit.exec()
                self._api.reply_message(
                    event.reply_token,
                    reply,
                )
                return
            except Exception:
                self._api.reply_message(event.reply_token, TextSendMessage(text='操作失敗\n'))
