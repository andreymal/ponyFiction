from ..models import Story
from .utils import BaseAPI


class StoryAPI(BaseAPI):

    _prefix = "story."

    @staticmethod
    def get_random(request):
        """Get random stories"""
        stories = Story.bl.get_random()
        return [s.to_dict({'title', 'url', 'summary', 'categories', 'characters', 'url'}) for s in stories]
