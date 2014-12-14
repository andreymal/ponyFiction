# encoding: utf8
import unittest
from ponyFiction.filters import filter_html, _filter_html, typo
from ponyFiction.filters.base import html_doc_to_string


class HtmlFiltersTests(unittest.TestCase):
    def test_filter_html_function(self):
        text = '<p>Дружба - это магия!</p>'
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