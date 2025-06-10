from common.exception import ValidationError
from common.error_code import ErrorCode
from consts.linebot_const import TextJobType


class AccountExecUnit:
    def __init__(self, text):
        self._text = text

    @staticmethod
    def _validate_text(text):
        if not isinstance(text, list):
            message = f"invalid type: {type(text)} of text"
            raise ValidationError(message=message, error_code=ErrorCode.DATA_ERROR)
        if text[0] != TextJobType.ACCOUNT:
            message = f"job: {text[0]} is invalid"
            raise ValidationError(message, error_code=ErrorCode.DATA_ERROR)

    @classmethod
    def exec(cls, text):
        cls._validate_text(text)
