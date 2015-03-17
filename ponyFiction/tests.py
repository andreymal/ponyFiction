# encoding: utf8
import unittest
from django.test import TestCase as DjangoTestCase
from ponyFiction.filters import filter_html, _filter_html, typo
from ponyFiction.filters.base import html_doc_to_string
from ponyFiction.models import Story, Author, Chapter
from ponyFiction.signals import story_viewed


class HtmlFiltersTests(unittest.TestCase):
    def test_filter_html_function(self):
        text = u'<p>Дружба - это магия!</p>'
        html_doc_to_string(filter_html(text))

    def test_href_validation(self):
        filter_html = lambda text: html_doc_to_string(
            _filter_html(
                text,
                tags = ['a'],
                attributes = { 'a': ['href'] }
            )
        )

        # Только абсолютные ссылки с протоколами http и https,
        # либо без указания протокола,
        # а так же ссылки на фрагменты в пределах страницы (начинающиеся на #)
        # считаются разрешёнными.
        valid_links = '''
            https://google.ru
            http://ya.ru
            //django.com/
            /stories/123/
            #comment12345
        '''
        for link in valid_links.split():
            src = '<a href="{}">click me</a>'.format(link)
            text = filter_html(src)
            self.assertEquals(text, src)

        invalid_links = '''
            javascript:alert(1);
            ftp://ftp.sourceforge.net/1.tar.gz
            gopher://example.com
        '''
        for link in invalid_links.split():
            text = filter_html('<a href="{}">click me</a>'.format(link))
            self.assertEquals(text, '<a>click me</a>')

    def test_typography_mdash(self):
        # В тексте дефис, отбитый пробелами, заменяется на тире с неразрывным пробелом
        self.assertEquals(typo(u'Дружба - это магия!'),u'Дружба\xa0\u2014 это магия!')

        # Дефис на тире в начале текста и в начале строки
        self.assertEquals(
            typo(
                u'- Louder!\n'
                u'- Yay!\n'
            ),
                u'\u2014 Louder!\n'
                u'\u2014 Yay!\n'
        )


class VoteIndicatorTests(unittest.TestCase):
    def get_indicator(self, o):
        return [
            s.replace('i/horseshoe-', '').replace('.png', '')
            for s in o.iter_horseshoe_images()
        ]

    def test_vote_ratio_indicator(self):
        o = Story()
        o.get_vote_rank = lambda: 1.0

        data = [
            (100, 0, ['l', 'r'] * 5),
            (100, 1, ['l', 'r'] * 5),
            (100, 100, ['l', 'r', 'l', 'r', 'l', 'rg', 'lg', 'rg', 'lg', 'rg']),
            (0, 100, ['lg', 'rg'] * 5),
            (80, 20, ['l', 'r'] * 4 + ['lg', 'rg']),
        ]

        for u, d, x in data:
            o.vote_up_count = u
            o.vote_down_count = d
            y = self.get_indicator(o)
            self.assertEquals(x, y, "up={} down={} r={}".format(u, d, y))


class ViewCounterTests(DjangoTestCase):
    def test_view_count(self):
        s = Story.objects.create()
        c = Chapter.objects.create(story = s)

        users = [
            Author.objects.create(username = 'user%s' % i)
            for i in range(3)
        ]
        for i in range(7):
            story_viewed.send(
                Author,
                instance = users[i%len(users)],
                story = s,
                chapter = c,
            )

        self.assertEqual(s.views, 3)
        self.assertEqual(s.story_views_set.count(), 7)
