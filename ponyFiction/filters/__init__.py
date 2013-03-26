import re
import functools
import bleach
from django.utils.safestring import mark_safe
from django.conf import settings
from ..utils.typographus import typo
from .base import html_doc_to_string
from .html import normalize_html



empty_lines_re = re.compile(r'\n[\s\n]*\n')

def filter_html(text,
                tags = settings.SANITIZER_ALLOWED_TAGS,
                attributes = settings.SANITIZER_ALLOWED_ATTRIBUTES):
    
    text = html_doc_to_string(normalize_html(text, convert_linebreaks = True))
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
    return property(fn)
    