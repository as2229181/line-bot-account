from redis.commands.json.path import Path

from config import Config
from middlewares.manager.base_manager import BaseManager
from middlewares.manager.redis_key import RedisKey


class AccountManager(BaseManager):
    def __init__(self):
        super().__init__(Config.ACCOUNT_DB_NUM)
        self._expire = Config.ACCOUNT_EXPIRED_TIME

    def set_session(self, user_uuid, value, expire=None):
        key = RedisKey.get_account_key(user_uuid)
        self._rd.json().set(key, Path.root_path(), value)
        self._rd.expire(key, expire or self._expire)

    def update_session(self, user_uuid, field, value):
        key = RedisKey.get_account_key(user_uuid)
        self._rd.json().set(key, Path(f'.{field}'), value)

    def get_session(self, user_uuid):
        key = RedisKey.get_account_key(user_uuid)
        return self._rd.json().get(key)

    def delete_session(self, user_uuid):
        key = RedisKey.get_account_key(user_uuid)
        self._rd.delete(key)
