import pygsheets
from config import Config
from common.exception import ExternalError

class _GoogleSheet:
    _TOKEN = Config.GOOGLE_AUTHORIZE_TOKEN
    _SHEET_ID = Config.GOOGLE_ID

    def __init__(self):
        self._spreadsheet = self._auth().open_by_key(self._SHEET_ID)

    def _auth(self):
        return pygsheets.authorize(client_secret=self._TOKEN)

    @property
    def spreadsheet(self):
        return self._spreadsheet


class GoogleSheetOperator:
    def __init__(self):
        self._spreadsheet = _GoogleSheet().spreadsheet
    
    def get_worksheets(self) -> list:
        return self._spreadsheet.worksheets()

    def get_worksheet(self, name):
        return self._spreadsheet.worksheet(
            property='title', 
            value=name,
        )        
    
    def delete_worksheet(self, name):
        sheet = self.get_worksheet(name=name)
        if sheet:
            msg = f'sheet: {name} is not exist'
            raise ExternalError(message=msg)
        self._spreadsheet.del_worksheet(sheet)
        return 'ok'
    
    def create_worksheet(self, name: str, rows: int=100, columns=26) -> pygsheets.Worksheet:
        """
        Creatre new work sheet 
        para: 
            name: worksheet name
            rows: set worksheet total rows, default is 100
            columns: set worksheet total column, default is 26
        return:
            pygsheets.worksheet
        """
        sheet = self.get_worksheet(name)
        if sheet:
            msg = f'sheet: {name} is not exist'
            raise ExternalError(message=msg)
        new_worksheet = self._spreadsheet.add_worksheet(
            name, 
            rows=rows, 
            cols=columns
        )
        return new_worksheet
    
    def set_column_name(self, worksheet: pygsheets.Worksheet, column_name: list[str]):
        column_len = len(column_name)
        if column_len > worksheet.cols:
            msg = 'exceed column length'
            raise ExternalError(message=msg)
        worksheet.update_row(
            index=1, 
            values=column_name,
        )

    def add_row(self, worksheet, value: list):
        
