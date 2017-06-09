"""
Metaclass example, which can add cache with common life time
(i.e. cache expires after that time) for all user methods.
"""

from time import sleep
from threading import Thread

class Meta(type):
    """ Class `Meta` implemented as metaclass, that inherits `type`.
        Used for overload magic method `__new__` to get a way
        of changing created class namespace.

        In the received namespace user methods are wrapped into
        a function of `Cache` class (see `Cache` docstring), that
        saves function result for a given time.

        Uncomment other magic methods to see a full chain."""

    # @classmethod
    # def __prepare__(mcs, name, bases, **kwargs):
    #     print('  Meta.__prepare__(mcs=%s, name=%r, bases=%s, kwargs=%s)\n'\
    #             % (mcs, name, bases, kwargs))
    #     return {}

    # def __init__(cls, name, bases, attrs, **kwargs):
    #     print('  Meta.__init__(cls=%s, name=%r, bases=%s, attrs=[%s], kwargs=%s)\n'\
    #             % (cls, name, bases, ', '.join(attrs), kwargs))
    #     super().__init__(name, bases, attrs)

    # def __call__(cls, *args, **kwargs):
    #     print('  Meta.__call__(cls=%s, args=%s, kwargs=%s)\n'\
    #             % (cls, args, kwargs))
    #     return super().__call__(*args, **kwargs)

    # def __getattribute__(cls, name):
    #     print("  Meta.__getattribute__, {}\n".format((cls, name)))
    #     return super().__getattribute__(name)

    # def __setattr__(cls, name, value):
    #     print("  Meta.__setattr__, {}\n".format((cls, name, value)))
    #     super().__setattr__(name, value)

    def __new__(mcs, name, bases, attrs, **kwargs):
        print('  Meta.__new__(mcs=%s, name=%r, bases=%s, attrs=[%s], kwargs=%s)\n'\
                % (mcs, name, bases, ', '.join(attrs), kwargs))
        if "Cache" in globals():
            Cache.delay = kwargs
            for k in attrs:
                if callable(attrs[k]) and k not in type.__dict__:
                    attrs[k] = Cache.get_cache(attrs[k])
        return super().__new__(mcs, name, bases, attrs)

class Cache(metaclass=Meta):
    """ Class `Cache` implemented as metaclass, that inherits `Meta`,
        written above.

        `get_cache` implemented, as a wrapper for given user methods.
        It allows to save function result in `cached` class variable.
        It also initiates cashe "cleaner" - `delayed_purge` - as separate
        thread, that clears saved result after given time."""

    cached = None
    delay = None

    @classmethod
    def get_cache(cls, user_method):
        def wrapper(*original_args, **original_kwargs):
            print(":::Wrapped:::")
            if cls.cached:
                print("===Taken===")
                return cls.cached
            cls.cached = user_method(*original_args, **original_kwargs)
            print("===Cached===")
            purge_thread = Thread(target=cls.delayed_purge)
            purge_thread.setDaemon(True)
            purge_thread.start()
            return cls.cached
        return wrapper

    @classmethod
    def delayed_purge(cls):
        sleep(cls.delay['memtime'])
        cls.cached = None
        print("===Purged===")

    # def __getattribute__(cls, name):
    #     print("In Cache.__getattribute__:\n->{}\n".format((cls, name)))
    #     return super().__getattribute__(name)


if __name__ == "__main__":

    class Foo(Cache, memtime=5):

        def __init__(self, x):
            self.x = x

        def mul(self, y):
            sleep(1)
            return self.x * y

    foo = Foo(100)
# First calculation.
    print(foo.mul(10))  # Takes 1 sec to get result.
                 # Result: 1000
# Second call with the same values return result from cache.
    print(foo.mul(10))  # Returns result immediately.
                 # Result: 1000
    sleep(5)
# Third call after 5 sec takes again about 1 sec.
    print(foo.mul(10))  # Takes 1 sec to get result again. Cache expired.
                 # Result: 1000
