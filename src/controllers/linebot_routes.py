from flask import Blueprint
from handlers.payload_fields import PayloadFields
from handlers.header_getter import HeaderGetter
from handlers.decorators import payload_check

line_bot_bp = Blueprint('line_bot', __name__)


@line_bot_bp.route('', methods=['POST'])
@payload_check(PayloadFields.linebot_schema)
def entry_point(payload):
    # TODO: Handle line bot message
    return 200
