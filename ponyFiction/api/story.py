from .utils import BaseAPI


class StoryAPI(BaseAPI):

    _prefix = "story."

    @staticmethod
    def get_random(request):
        """Get random story"""
        return [
            {
                "name": "test"
            }
        ]
