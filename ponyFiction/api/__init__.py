from jsonrpc import Dispatcher
from .story import StoryAPI

__all__ = ("dispatcher",)

dispatcher = Dispatcher()

StoryAPI(dispatcher)
