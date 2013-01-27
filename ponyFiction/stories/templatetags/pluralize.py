# -*- coding: utf-8 -*-
from django import template
register = template.Library()
@register.filter
def rupluralize(value, arg='число,числа,чисел'):
    args = arg.split(',')
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if number == 0:
        return 'нет %s' % args[2]
    if (a == 1) and (b != 11):
        return '%s %s' % (number, args[0])
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return '%s %s' % (number, args[1])
    else:
        return '%s %s' % (number, args[2])