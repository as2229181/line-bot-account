from flask import current_app

from consts.linebot_const import TextJobType
from middlewares.webhook.text_units.account.account_exec_unit import AccountExecUnit
from middlewares.webhook.text_units.help.help_exec_unit import HelpExecUnit


class TextDispatcher:
    _JOB_DICT = {
        TextJobType.HELP: HelpExecUnit,
        TextJobType.ACCOUNT: AccountExecUnit,
    }

    @staticmethod
    def _extract_text_with_no_session(text):
        """
        split text message and transfer to dict
        """
        raw_text = text.strip()
        if ' ' in raw_text:
            command_part, params = raw_text.split(' ', 1)
        else:
            command_part, params = raw_text, None

        command_token = command_part.split('-')

        job = command_token[0]
        action = command_token[1] if len(command_token) > 1 else None
        return job, action, params

    @classmethod
    def dispatch(cls, text, user_uuid):
        account_manager = getattr(current_app, 'account_manager', None)
        if not account_manager:
            return None
        job, action, params = cls._extract_text_with_no_session(text)
        account_session = account_manager.get_session(user_uuid)
        if account_session:
            exec_unit = cls._JOB_DICT[TextJobType.ACCOUNT]
            return exec_unit(user_uuid, text, params, action)

        exec_unit = cls._JOB_DICT.get(job, None)

        if not exec_unit:
            return None

        return exec_unit(user_uuid, text, params, action)
