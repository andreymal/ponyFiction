#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from unidecode import unidecode

def _monkey_patch():
    import unidecode.x004
    data = dict((chr(i+0x400), x) for i, x in enumerate(unidecode.x004.data))
    
    data.update({
        'й': 'y',
        'ю': 'y',
        'я': 'ya',
        'ё': 'yo',
        'Й': 'Y',
        'Ю': 'Y',
        'Я': 'Ya',
        'Ё': 'Yo',
    })
    
    unidecode.x004.data = tuple(x for _, x in sorted(data.items()))
    
_monkey_patch()
