from importlib import import_module

from flask_migrate import Migrate

from app import app
from config import Config
from core import create_app, db

import_module('models')
app = create_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='127.0.0.1', port=6789)
