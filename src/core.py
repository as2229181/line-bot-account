from flask_compress import Compress
from flask_cors import CORS

from config import Config
from services.linebot_service import LineBotService


def _init_service(app):
    """
    init linebot service
    """
    linebot_service = LineBotService(
        access_token=Config.LINEBOT_ACCESS_TOKEN,
        secret=Config.LINEBOT_SECRET,
    )
    setattr(app, 'linebot_service', linebot_service)


def _init_database():
    """
    init database(redis or ??)
    """


def _init_log():
    """
    init log system
    """


def _register_controller(app):
    """
    register controller
    """
    from controllers.linebot_routes import line_bot_bp
    app.register_blueprint(line_bot_bp, url_prefix='/line-bot')


def _register_prob(app):
    @app.route('/probe', methods=['GET'])
    def probe():
        return 'ok'


def create_app(_app):
    CORS(_app, send_wildcard=True)
    Compress(_app)
    _init_service(_app)
    _init_database()
    _init_log()
    _register_controller(_app)
    _register_prob(_app)
    return _app
