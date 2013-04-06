# encoding: utf8 
from __future__ import absolute_import
from unidecode import unidecode

def _monkey_patch():
    import unidecode.x004
    data = dict((unichr(i+0x400), x) for i, x in enumerate(unidecode.x004.data))
    
    data.update({
        u'й': 'y',
        u'ю': 'yu',
        u'я': 'ya',
        u'ё': 'yo',
        u'Й': 'Y',
        u'Ю': 'Yu',
        u'Я': 'Ya',
        u'Ё': 'Yo',
    })
    
    unidecode.x004.data = tuple(x for _, x in sorted(data.items()))
    
_monkey_patch()