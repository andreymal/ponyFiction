import re
from django import template

register = template.Library()

RE_NORMALIZE = re.compile(r"\W+")

try:
    _version = open("backend.version").read().strip()
except (IOError, OSError) as e:
    _version = "dev"


@register.filter
def normspaces(value):
    return RE_NORMALIZE.sub(" ", value).strip()


@register.simple_tag
def version():
    return _version
