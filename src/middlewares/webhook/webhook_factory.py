from webhook.message_job import MessageJob
from consts.linebot_const import EventType
from common.error_code import ErrorCode
from common.exception import ValidationError


class WebHookFactoy:
    _FACTOY = {
        EventType.MESSAGE: MessageJob,
    }

    @classmethod
    def get_exec_unit(cls, _type, message):
        factory = cls._FACTOY.get(EventType.MESSAGE, None)

        if not factory:
            message = f"event type: {_type} now is not open"
            raise ValidationError(message, error_code=ErrorCode.INVALID_OPERATION)
        exec_unit = factory.get_unit(message)
        return exec_unit
