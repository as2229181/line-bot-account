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


class WorkSheetsColumnName(ConstBase):
    UUID = 'uuid'                      # 唯一識別碼
    DATE = 'date'                      # 交易日期
    AMOUNT = 'amount'                  # 交易金額（正數或負數）
    DESCRIPTION = 'description'        # 備註／摘要
    BALANCE = 'balance'                # 結餘（使用公式計算）
    USER = 'user'                # 記帳人識別
    CREATED_AT = 'created_at'          # 建立時間
    UPDATED_AT = 'updated_at'          # 最後更新時間
