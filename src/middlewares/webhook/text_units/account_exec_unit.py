from common.exception import ValidationError
from common.error_code import ErrorCode
from consts.linebot_const import TextJobType
from datetime import datetime
from middlewares.google_sheet.google_sheet_operator import GoogleSheetOperator


class AccountExecUnit:
    def __init__(self, text):
        self._text = text
        self._title = self._get_title()
        self._sheet_operator = GoogleSheetOperator(self._title)

    @staticmethod
    def _get_title():
        cur = datetime.now()
        cur_year, cur_month = cur.year, cur.month
        return f'{cur_year}-{cur_month:02d}'

    def _validate_text(self):
        text = self._text
        if not isinstance(text, list):
            message = f'invalid type: {type(text)} of text'
            raise ValidationError(message=message, error_code=ErrorCode.DATA_ERROR)
        if text[0] != TextJobType.ACCOUNT:
            message = f'job: {text[0]} is invalid'
            raise ValidationError(message, error_code=ErrorCode.DATA_ERROR)

    def exec(self):
        self._validate_text()
        sheet_operator = self._sheet_operator
        sheet_operator.set_column_names()
        return
