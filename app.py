from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from config import Config
from services.linebot_service import LineBotService

app = Flask(__name__)

CORS(app, send_wildcard=True)
Compress(app)


def _init_service():
    """
    init linebot service
    """
    linebot_service = LineBotService(
        access_token=Config.LINEBOT_ACCESS_TOKEN,
        secret=Config.LINBOT_SECRET,
    )
    setattr(app, "linebot_service", linebot_service)


def _init_database():
    """
    init database(redis or ??)
    """


def _init_log():
    """
    init log system
    """


def _register_controller():
    """
    register controller
    """


def create_app():
    app.config.from_object(Config)
    _init_service()
    _init_database()
    _init_log()
    _register_controller()
    return app
