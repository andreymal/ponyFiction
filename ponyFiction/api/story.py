from . import api


@api.dispatcher.add_method("story.get_random")
def get_random(request):
    return [
        {
            "name": "test"
        }
    ]
