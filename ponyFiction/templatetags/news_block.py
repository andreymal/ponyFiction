from ponyFiction.models import NewsItem
from ponyFiction.templatetags.random_stories import register


@register.inclusion_tag('includes/news_block.html')
def news_block():
    item = NewsItem.bl.suggest()
    return {'item': item}
