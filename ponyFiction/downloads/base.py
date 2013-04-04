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
        return reverse(
            'ponyFiction.views.stories.story_download',
            kwargs = dict(
                story_id = story.id,
                filename = slugify(story.title),
                extension = self.extension,
            )
        )
        
        
class ZipFileDownloadFormat(BaseDownloadFormat):
    def render(self, **kw):
        import zipfile
        from cStringIO import StringIO
        
        buf = StringIO()
        zf = zipfile.ZipFile(buf, mode = 'w', compression = zipfile.ZIP_DEFLATED)
        try:
            self.render_zip_contents(zf, **kw)
        finally:
            zf.close()
    
        return buf.getvalue() 
        
        
def slugify(s):
    from ..utils.unidecode import unidecode
    return re.subn(r'\W+', '_', unidecode(s))[0]
