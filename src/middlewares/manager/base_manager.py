from redis import Redis

from config import Config


class BaseManager:
    def __init__(self, db_num):
        self._rd = Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=db_num,
            decode_responses=True,
        )
