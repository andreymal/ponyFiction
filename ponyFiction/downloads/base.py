#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from django.urls import reverse
from django.template.loader import render_to_string


class BaseDownloadFormat(object):
    extension = None
    name = None
    debug_content_type = 'text/plain'
    chapter_template = None
    chapter_extension = None

    def __init__(self):
        assert self.extension is not None
        assert self.name is not None

    def url(self, story):
        return reverse(
            'story_download',
            kwargs=dict(
                story_id=story.id,
                filename=slugify(story.title or str(story.id)),
                extension=self.extension,
            )
        )

    @property
    def slug(self):
        return slugify(str(self.name.lower()))


class ZipFileDownloadFormat(BaseDownloadFormat):
    chapter_encoding = 'utf8'

    def render(self, **kw):
        import zipfile
        from io import BytesIO

        buf = BytesIO()
        zf = zipfile.ZipFile(buf, mode='w', compression=zipfile.ZIP_DEFLATED)
        try:
            self.render_zip_contents(zf, **kw)
        finally:
            zf.close()

        return buf.getvalue()

    def render_zip_contents(self, zipfile, story, filename, **kw):
        ext = self.chapter_extension

        chapters = story.chapter_set.order_by('order')
        num_width = len(str(chapters.count()))
        for i, chapter in enumerate(chapters.iterator()):
            data = render_to_string(
                self.chapter_template,
                {
                    'chapter': chapter,
                    'story': story,
                },
            ).encode(self.chapter_encoding)

            name = slugify(chapter.title)
            num = str(i+1).rjust(num_width, '0')
            arcname = str('%s/%s_%s.%s' % (filename, num, name, ext))

            zipfile.writestr(arcname, data)


def slugify(s):
    from ..utils.unidecode import unidecode
    return re.subn(r'\W+', '_', unidecode(s))[0]
