from flask import Blueprint, request
from handlers.payload_fields import PayloadFields
from handlers.header_getter import HeaderGetter
from handlers.decorators import payload_check

line_bot_bp = Blueprint("line_bot", __name__)


@line_bot_bp.route("", methods=["POST"])
@payload_check(PayloadFields.linebot_schema)
def entry_point(payload):
    x_line_signature = HeaderGetter.get_x_line_signature()
