class RedisKey:
    @staticmethod
    def get_account_key(username):
        return f'account:{username}'
