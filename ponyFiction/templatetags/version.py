from django import template

register = template.Library()

try:
    _version = open("ponyFiction/VERSION").read().strip()
except (IOError, OSError) as e:
    _version = "dev"


@register.simple_tag
def version():
    return _version
