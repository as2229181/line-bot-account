from urllib.parse import quote

from flask import jsonify
from flask_compress import Compress
from flask_cors import CORS
from sqlalchemy import text

from config import Config
from database import db
from services.linebot_service import LineBotService


def _init_service(app):
    """
    init line_bot service
    """
    line_bot_service = LineBotService(
        access_token=Config.LINEBOT_ACCESS_TOKEN,
        secret=Config.LINEBOT_SECRET,
    )
    setattr(app, 'line_bot_service', line_bot_service)


def _init_manager(app):
    """
    init manager
    """
    from middlewares.manager.account_manager import AccountManager
    from middlewares.manager.user_manager import UserManager

    setattr(app, 'account_manager', AccountManager())
    setattr(app, 'user_manager', UserManager())


def _init_database(app):
    """
    init database
    """
    user = quote(Config.POSTGRES_USER)
    password = quote(Config.POSTGRES_USER_PASS)
    host = Config.POSTGRES_HOST
    port = Config.POSTGRES_PORT
    db_name = Config.DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    db.init_app(app)


def _init_log(app):
    """
    init log system
    """
    # TODO: add logger to elasticsearch
    from common.debug_tool import DebugTool

    DebugTool.add_file_logger(tag='line_bot_account')
    DebugTool.start_logging()


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

    @app.route('/probe/postgres', methods=['GET'])
    def postgres_probe():
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text('SELECT 1')).scalar()
            if result == 1:
                return jsonify(status='ok'), 200
            else:
                return jsonify(status='unexpected result'), 500
        except Exception as e:
            return jsonify(status='error', detail=str(e)), 500


def create_app(_app):
    CORS(_app, send_wildcard=True)
    Compress(_app)
    _init_service(_app)
    _init_manager(_app)
    _init_database(_app)
    _init_log(_app)
    _register_controller(_app)
    _register_prob(_app)
    return _app
