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
        secret=Config.LINBOT_SECRET,
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


def create_app(app):
    CORS(app, send_wildcard=True)
    Compress(app)
    _init_service(app)
    _init_database()
    _init_log()
    _register_controller(app)
    return app
