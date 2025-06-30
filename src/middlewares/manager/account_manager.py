from redis.commands.json.path import Path

from config import Config
from middlewares.manager.base_manager import BaseManager
from middlewares.manager.redis_key import RedisKey


class AccountManager(BaseManager):
    def __init__(self):
        super().__init__(Config.ACCOUNT_DB_NUM)

    def set_session(self, username, value):
        key = RedisKey.get_account_key(username)
        self._rd.json(key, Path.root_path(), value)

    def update_session(self, username, field, value):
        key = RedisKey.get_account_key(username)
        self._rd.json(key, Path(f'.{field}'), value)

    def get_session(self, username):
        key = RedisKey.get_account_key(username)
        return self._rd.json().get(key)

    def delete_session(self, username):
        key = RedisKey.get_account_key(username)
        self._rd.delete(key)
