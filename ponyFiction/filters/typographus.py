import re
from .base import html_text_transform


typo_patterns = [
    (r'(\n|^)-\s+', u'\\1\u2014 '),
    (r'\s+-\s+', u'\xa0\u2014 '),
]
typo_patterns = [(re.compile(p), r) for p, r in typo_patterns]

@html_text_transform
def typo(text):
    for p, r in typo_patterns:
        text = p.subn(r, text)[0]
    return text