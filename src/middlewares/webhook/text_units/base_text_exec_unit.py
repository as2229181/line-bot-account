class BaseTextExecUnit:
    def __init__(self, user_uuid, input_text, params=None, action=None):
        self._user_uuid = user_uuid
        self._input_text = input_text
        self._params = params
        self._action = action

    def exec(self):
        raise NotImplementedError
