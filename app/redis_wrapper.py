from redis import StrictRedis


# Redis wrapper class for convenience when running unit tests
class RedisWrapper():

    def __init__(self, test=True):
        self.test = test

        # If testing mode is active, use a dict instead of trying to connect
        if not test:
            self.redis = StrictRedis(host='redis')
        else:
            self.redis = dict()

    def get(self, name):
        if not self.test:
            return self.redis.get(name)
        else:
            return self.redis[name]

    def set(self, name, value):
        if not self.test:
            self.redis.set(name, value)
        else:
            self.redis[name] = value

    def exists(self, name):
        if not self.test:
            return self.redis.exists(name)
        else:
            return name in self.redis

    def expireat(self, name, when):
        # No such thing as expiry for testing mode
        if not self.test:
            self.redis.expireat(name, when)

    def delete(self, name):
        if not self.test:
            self.redis.delete(name)
        else:
            self.redis.pop(name)
