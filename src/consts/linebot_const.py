from linebot.models import UnfollowEvent
from linebot.models.events import Unsend
from common import const_base
from common.const_base import ConstBase


class EventType(const_base):
    MESSAGE = "message"
    UNSEND = "unsend"
    FLOLLOW = "flollow"
    UNFOLLOW = "unfollow"
    JOIN = "join"
    LEAVE = "leave"
    MEMBER_JOIN = "member_jon"
    MEMBER_LEAVE = "member_leave"
    POSTBACK = "postback"
    VIDEO = "video"


class MessageType(ConstBase):
    TEXT = "text"
    IMAGE = "image"
    STICKER = "sticker"


class TextJobType:
    ACCOUNT = "account"
