class RedisKey:
    @staticmethod
    def get_account_key(user_uuid):
        return f'account:{user_uuid}'

    @staticmethod
    def get_create_user_key(user_uuid):
        return f'user:create:{user_uuid}'
