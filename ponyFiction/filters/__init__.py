import re
import functools
import bleach
from django.utils.safestring import mark_safe
from django.conf import settings
from ..utils.typographus import typo
from .base import html_doc_to_string
from .html import normalize_html, footnotes_to_html



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
    return text
    
def filtered_html_property(name, filter_):
    def fn(self):
        return mark_safe(html_doc_to_string(filter_(getattr(self, name))))
    return property(fn)
    