class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseAPI(metaclass=Singleton):
    _prefix = ""
    _dispatcher = None

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher
        dispatcher.build_method_map(self, self._prefix)
