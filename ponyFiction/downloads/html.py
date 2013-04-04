from .base import ZipFileDownloadFormat, slugify
from django.template.loader import render_to_string

class HTMLDownload(ZipFileDownloadFormat):
    extension = 'html.zip'
    name = 'HTML'
    
    def render_zip_contents(self, zipfile, story, filename, **kw):
        chapters = story.chapter_set.order_by('order')
        num_width = len(str(chapters.count()))
        for i, chapter in enumerate(chapters.iterator()):
            data = render_to_string(
                'chapter_pure_html.html',
                {
                    'chapter': chapter,
                    'story': story,
                },
            ).encode('utf8')
            
            name = slugify(chapter.title)
            num = str(i+1).rjust(num_width, '0')
            arcname = str('%s/%s_%s.html' % (filename, num, name))
            
            zipfile.writestr(arcname, data)