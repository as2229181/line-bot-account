from schema import And, Optional, Schema
from handlers.schema_validator import SchemaValidator

_ALLOW_TYPE = ["text", "image", "video", "audio", "location", "sticker"]


class PayloadFields:
    linebot_schema = Schema(
        {
            "type": And(str, lambda t: t in _ALLOW_TYPE),
            "id": str,
            Optional("text"): And(
                str,
                SchemaValidator.is_not_empty,
            ),
        }
    )
