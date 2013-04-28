from ponyFiction.models import Story
from django import template
register = template.Library()

@register.inclusion_tag('includes/random_stories.html')
def random_stories():
    random_stories = Story.objects.published.order_by('?').cache()[0:10]
    return {'random_stories': random_stories}