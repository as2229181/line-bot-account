
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

app = Flask(__name__)

CORS(app, send_wildcard=True)
Compress(app)


def _init_service():
    """
    init linebot service
    """


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
    _init_service()
    _init_database()
    _init_log()
    _register_controller()
    return app
