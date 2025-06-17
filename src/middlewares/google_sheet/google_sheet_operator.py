import pygsheets

from common.exception import ExternalError
from config import Config
from consts.linebot_const import WorkSheetsColumnName


class _GoogleSheet:
    _TOKEN_FILE = Config.GOOGLE_CLIENT_SECRET_FILE_PATH
    _SHEET_URL = Config.GOOGLE_SHEET_URL

    def __init__(self):
        self._spreadsheet = self._auth().open_by_url(self._SHEET_URL)

    def _auth(self):
        return pygsheets.authorize(service_account_file=self._TOKEN_FILE)

    @property
    def spreadsheet(self):
        return self._spreadsheet


class GoogleSheetOperator:
    def __init__(self, title):
        self._spreadsheet = _GoogleSheet().spreadsheet
        self._worksheet = self._get_worksheet(name=title)
        self.set_column_names()

    def get_worksheets(self) -> list:
        return self._spreadsheet.worksheets()

    def _get_worksheet(self, name):
        try:
            return self._spreadsheet.worksheet(property='title', value=name)
        except pygsheets.WorksheetNotFound:
            return self.create_worksheet(name=name)

    def delete_worksheet(self, name):
        sheet = self._get_worksheet(name=name)
        if sheet:
            msg = f'sheet: {name} is not exist'
            raise ExternalError(message=msg)
        self._spreadsheet.del_worksheet(sheet)
        return 'ok'

    def create_worksheet(self, name: str, rows: int = 100, columns=26) -> pygsheets.Worksheet:
        new_worksheet = self._spreadsheet.add_worksheet(title=name, rows=rows, cols=columns)
        return new_worksheet

    def set_column_names(
        self,
    ):
        sheet = self._worksheet
        first_row = sheet.get_row(1, include_tailing_empty=False)
        if any(val.strip() for val in first_row):
            return

        column_names = WorkSheetsColumnName.get_values()

        sheet.update_row(index=1, values=column_names)

    def add_row(self, title: str, values: list) -> None:
        sheet = self._spreadsheet.worksheet(property='title', value=title)
        if not sheet:
            msg = f'sheet: {title} does not exist'
            raise ExternalError(message=msg)

        filled_rows = sheet.get_all_values(include_empty=False)
        next_index = len(filled_rows) + 1

        sheet.update_row(index=next_index, values=values)
