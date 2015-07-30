from .utils import BaseAPI


class StoryAPI(BaseAPI):

    _prefix = "story."

    @staticmethod
    def get_random(request):
        """Get random stories"""
        return [
            {
                "title": "First story",
                "url": "/story/1",
                "summary": "Short summary",
                "thumb": None,
                "categories": [
                    {
                        "name": "Lorem",
                        "url": "/category/1",
                        "color": "#3465a4",
                    },
                    {
                        "name": "Ipsum",
                        "url": "/category/2",
                        "color": "#edd400",
                    },
                ],
                "characters": [
                    {
                        "name": "Hero 1",
                        "url": "/character/1",
                        "thumb": "/static/img/7f154d566c.png"
                    }
                ]
            }
        ]
