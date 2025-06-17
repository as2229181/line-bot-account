from common.error_code import ErrorCode
from common.exception import ValidationError
from consts.linebot_const import TextJobType
from middlewares.webhook.text_units.account_exec_unit import AccountExecUnit


class TextActor:
    _JOB_DICT = {
        TextJobType.ACCOUNT: AccountExecUnit,
    }

    @staticmethod
    def _extract_text_to_list(message) -> list:
        text = message.get("text").split()
        return text

    @classmethod
    def get_unit(cls, message):
        text = cls._extract_text_to_list(message)
        job = text[0]
        exec_unit = cls._JOB_DICT.get(job, None)
        if not exec_unit:
            message = f"Job: {job} is not been define"
            raise ValidationError(message, error_code=ErrorCode.INVALID_OPERATION)
        return exec_unit(text)
