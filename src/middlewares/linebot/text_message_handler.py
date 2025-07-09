from flask import current_app
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from consts.linebot_const import TextJobType
from middlewares.linebot.linebot_base_handler import LineBotBaseHandler
from middlewares.webhook.text_units.account.account_exec_unit import AccountExecUnit
from middlewares.webhook.text_units.help.help_exec_unit import HelpExecUnit
from middlewares.webhook.text_units.user.user_exec_unit import UserExecUnit


class TextMessageHandler(LineBotBaseHandler):
    _JOB_DICT = {
        TextJobType.HELP: HelpExecUnit,
        TextJobType.ACCOUNT: AccountExecUnit,
        TextJobType.USER: UserExecUnit,
    }

    def __init__(self, line_bot_api, line_bot_handler):
        super().__init__(line_bot_api, line_bot_handler)

    @staticmethod
    def _extract_text_with_no_session(text):
        """
        split text message and transfer to dict
        """
        raw_text = text.lower().strip()
        if ' ' in raw_text:
            command_part, params = raw_text.split(' ', 1)
        else:
            command_part, params = raw_text, None

        command_token = command_part.split('-')

        job = command_token[0]
        action = command_token[1] if len(command_token) > 1 else None
        return job, action, params

    @classmethod
    def _dispatch(cls, text, user_uuid):
        account_manager = getattr(current_app, 'account_manager', None)
        user_manager = getattr(current_app, 'user_manager', None)

        if not account_manager or not user_manager:
            return None
        job, action, params = cls._extract_text_with_no_session(text)

        account_session = account_manager.get_session(user_uuid)
        if account_session:
            exec_unit = cls._JOB_DICT[TextJobType.ACCOUNT]
            return exec_unit(user_uuid, text, params, action)

        create_user_session = user_manager.get_create_session(user_uuid)
        if create_user_session:
            exec_unit = cls._JOB_DICT[TextJobType.USER]
            return exec_unit(user_uuid, text, params, action)

        exec_unit = cls._JOB_DICT.get(job, None)
        if not exec_unit:
            return None

        return exec_unit(user_uuid, text, params, action)

    def register(self):
        @self._handler.add(MessageEvent, message=TextMessage)
        def handle(event):
            text = event.message.text
            user_uuid = event.source.user_id
            exec_unit = self._dispatch(text, user_uuid)
            if exec_unit is None:
                self._api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='❌ 請確認指令是否正確。'),
                )
                return
            try:
                reply = exec_unit.exec()
                self._api.reply_message(
                    event.reply_token,
                    reply,
                )
                return
            except Exception as e:
                print(e)
                self._api.reply_message(event.reply_token, TextSendMessage(text='操作失敗'))
