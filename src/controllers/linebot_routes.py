from flask import Blueprint, current_app, request
from linebot.exceptions import BaseError

line_bot_bp = Blueprint('line_bot', __name__)


@line_bot_bp.route('', methods=['POST'])
def entry_point():
    # TODO: Handle line bot message
    line_bot_service = getattr(current_app, 'line_bot_service', None)
    if not line_bot_service:
        return 'line_bot_service not found', 200

    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        line_bot_service.handler.handle(body, signature)
    except BaseError as e:
        # TODO 更精細的 error catch
        print(f'LINE SDK error caught: {e}', flush=True)
        return f'lint bot failed: {e}', 200
    except Exception as e:
        print(f'handler failed: {e}', flush=True)
        return f'handler failed: {e}', 200
    return 'ok', 200
