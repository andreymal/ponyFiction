from ponyFiction.models import Story
from django import template
register = template.Library()

@register.simple_tag
def submitted_stories_count():
    return Story.objects.filter(draft=False, approved=False).count()