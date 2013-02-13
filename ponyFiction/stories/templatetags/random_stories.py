from ponyFiction.stories.models import Story
from django import template
register = template.Library()

@register.inclusion_tag('random_stories.html')
def random_stories():
    random_stories = Story.published.order_by('?')[0:10]
    return {'random_stories': random_stories}