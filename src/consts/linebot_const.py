from common.const_base import ConstBase


class EventType(ConstBase):
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
