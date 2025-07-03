class RedisKey:
    @staticmethod
    def get_account_key(user_uuid):
        return f'account:{user_uuid}'
