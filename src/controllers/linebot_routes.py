from flask import Blueprint

from handlers.decorators import payload_check
from handlers.payload_fields import PayloadFields

line_bot_bp = Blueprint('line_bot', __name__)


@line_bot_bp.route('', methods=['POST'])
@payload_check(PayloadFields.linebot_schema)
def entry_point(payload):
    # TODO: Handle line bot message
    return 200
