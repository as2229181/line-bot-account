from gevent import monkey

monkey.patch_all()

from app import app
from config import Config
from core import create_app

app = create_app(app)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5555)
