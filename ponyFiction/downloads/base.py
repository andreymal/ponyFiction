import re
from django.core.urlresolvers import reverse

class BaseDownloadFormat(object):
    extension = None
    name = None
    debug_content_type = 'text/plain'
    
    def __init__(self):
        assert self.extension is not None
        assert self.name is not None
    
    def url(self, story):
        from unidecode import unidecode
        return reverse(
            'ponyFiction.views.stories.story_download',
            kwargs = dict(
                story_id = story.id,
                filename = re.subn(r'\W+', '_', unidecode(story.title))[0],
                extension = self.extension,
            )
        )
        