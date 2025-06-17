class LineBotBaseHandler:
    def __init__(self, line_bot_api, line_bot_handler):
        self._api = line_bot_api
        self._handler = line_bot_handler

    def register(self):
        raise NotImplementedError

