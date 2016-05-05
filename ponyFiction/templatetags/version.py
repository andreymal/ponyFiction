from os.path import dirname
from os.path import join

from django import template

register = template.Library()

try:
    _version = open(join(dirname(dirname(__file__)), "VERSION")).read().strip()
except (IOError, OSError) as e:
    _version = "dev"


@register.simple_tag
def version():
    return _version
