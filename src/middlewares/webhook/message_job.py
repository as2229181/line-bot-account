from middlewares.webhook.text_units.text_actor import TextActor
from consts.linebot_const import MessageType


class MessageJob:
    _JOB_DICT = {
        MessageType.TEXT: TextActor,
    }

    @classmethod
    def get_exec_unit(cls, message):
        _type = message.get("type")
        message_actor = cls._JOB_DICT.get(_type)
        exec_unit = message_actor.get_unit(message)
        return exec_unit
