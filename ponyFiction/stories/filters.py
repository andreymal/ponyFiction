import re
import bleach
from django.conf import settings
from django.utils.safestring import mark_safe
from .utils.typographus import typo

empty_lines_re = re.compile(r'\n[\s\n]*\n')

def filter_html(text):
    text = '<p>%s</p>' % (empty_lines_re.subn('</p><p>', text)[0])
    text = text.replace('\n', '<br>')
    text = typo(text)
    text = bleach.clean(text,
        tags = settings.SANITIZER_ALLOWED_TAGS,
        attributes = settings.SANITIZER_ALLOWED_ATTRIBUTES
    ) 
    return mark_safe(text)
    
def filtered_property(name, filter_):
    def fn(self):
        return filter_(getattr(self, name))
    return fn
    