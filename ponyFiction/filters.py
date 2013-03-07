import re
import functools
import bleach
from django.conf import settings
from django.utils.safestring import mark_safe
from .utils.typographus import typo

empty_lines_re = re.compile(r'\n[\s\n]*\n')

def filter_html(text,
                tags = settings.SANITIZER_ALLOWED_TAGS,
                attributes = settings.SANITIZER_ALLOWED_ATTRIBUTES):
    
    text = '<p>%s</p>' % (empty_lines_re.subn('</p><p>', text)[0])
    text = text.replace('\n', '<br>')
    text = typo(text)
    text = bleach.clean(text,
        tags = tags,
        attributes = attributes
    ) 
    return mark_safe(text)

filter_chapter_html = functools.partial(filter_html,
                                        tags = settings.SANITIZER_CHAPTER_ALLOWED_TAGS,
                                        attributes = settings.SANITIZER_CHAPTER_ALLOWED_ATTRIBUTES)
    
def filtered_property(name, filter_):
    def fn(self):
        return filter_(getattr(self, name))
    return fn
    