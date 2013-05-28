# -*- coding: utf-8 -*-

def pagination_ranges(
    num_pages,             # sumary page numbers
    page,                  # current page number [1...num_pages] or <=0 if none
    reverse=False,         # reverse enumeration
    show_all=False,        # show all pages
    fixed_locality=False,  # always fixed locality size
    head=3,                # pages in head (>=0)
    locality=5,            # locality of current page (>=0)
    tail=3,                # pages in tail (>=0)
    stick=1                # stick interval (>=0)
):

    """
    get pretty paginator ranges
    return 3 ranges of indexes [1...num_pages] and 2 dots flags
    (head_range, dots1, locality_range, dots2, tail_range)

    Example #1 (num_pages=20, page=10, reverse=False):
       1 2 3 ... 8 9 10 11 12 ... 17 18 19 20
       ^^^^^  |  ^^^^^^^^^^^^  |  ^^^^^^^^^^^
      head=3  |  locality=5    |  tail=4
         dots1=True       dots2=True

    Example #2 (num_pages=10, page=0 or locality=0, reverse=True):
       10 9 8 7 ... 3 2 1
       ^^^^^^^^  |  ^^^^^
       head=4    |  tail=3
            dots1=True
            dots2=False

    Example #3 (num_pages=10, reverse=False):
       1 2 3 4 5 6 7 8 9 10
       ^^^^^^^^^^^^^^^^^^^^
       head=10
       dots1=dots2=False, locality=tail=0
    """

    if not stick or stick < 0:
        stick = 0

    if head + tail + stick >= num_pages or show_all:
        # `head` cross `tail`, show all pages
        head = num_pages
        locality = start = finish = tail = 0
    else:
        if reverse:
            (head, tail) = (tail, head)

    # transform (`page`, `locality`) to (`start`, `finish`)
    if page >= 1 and page <= num_pages and locality > 0:
        if fixed_locality:
            # locality always has fixed length
            if not reverse:
                start = page - (locality - 1) / 2
            else:
                start = page - locality / 2
            if start < 1:
                start = 1
            finish = start + locality - 1
            if finish > num_pages:
                finish = num_pages
                start = num_pages - locality + 1
            if start < 1:
                start = 1
            locality = finish + 1 - start
        else:
            # locality may shortly near first or last page
            if not reverse:
                start = page - (locality - 1) / 2
                finish = page + locality / 2
            else:
                start = page - locality / 2
                finish = page + (locality - 1) / 2
            if start < 1:
                start = 1
            if finish > num_pages:
                finish = num_pages
            locality = finish + 1 - start
    else:
        locality = start = finish = 0

    # check head and locality overlay
    if head >= finish:
        # `head` cover `locality` => avoid locality
        locality = start = finish = 0
    elif head + stick + 1 >= start:
        # `head` cross `locality` => combine them to `head`
        head = finish
        locality = start = finish = 0

    # check locality and tail overlay
    if head + tail + stick >= num_pages:
        # `head` cross `tail` => show all pages as `head`
        head = num_pages
        locality = start = finish = tail = 0
    elif start > num_pages - tail:
        # `tail` cover `locality` => avoid locality
        locality = start = finish = 0
    elif finish + stick >= num_pages - tail:
        # `tail` cross `locality` => combine them to `tail`
        tail = num_pages - start + 1
        locality = start = finish = 0

    if head + tail + stick >= num_pages:
        # `head` cross `tail` => show all pages as `head`
        head = num_pages
        locality = start = finish = tail = 0

    if not reverse:
        head_range = xrange(1, head + 1)
        locality_range = xrange(start, start + locality)
        tail_range = xrange(num_pages + 1 - tail, num_pages + 1)
    else:
        head_range = xrange(num_pages, num_pages - tail, -1)
        locality_range = xrange(finish, finish - locality, -1)
        tail_range = xrange(head, 0, -1)

    head_dots = bool(head_range and (locality_range or tail_range))
    tail_dots = bool(locality_range and tail_range)
    pagination = {
        'current': page,
        'head_range': head_range,
        'head_dots': head_dots,
        'locality_range': locality_range,
        'tail_dots': tail_dots,
        'tail_range': tail_range
    }
    return pagination


def unicode_to_int_list(lst):
    '''
    [u'1', u'2', u'3', u'4'] → [1, 2, 3, 4]
    '''
    try:
        return map(lambda x: int(x), lst)
    except:
        return False

unicode_to_bool_list = lambda n: map(lambda x: bool(int(x)), n)
# [u'1', u'0', u'0', u'1'] → [True, False, False, True]

obj_to_int_list = lambda n: map(lambda x: int(x.id), n)
# [<obj_one>, <obj_two>, <obj_three>, <obj_four>] → [1, 2, 3, 4]


# Функции берут данные с POST-формы, и проставляют фильтры Sphinx, возвращая словарь новых начальных данные

def SetBoolSphinxFilter(sphinx, filter_name, field_name, oldform):
    filters = oldform.cleaned_data[field_name]
    try:
        selector = unicode_to_bool_list(filters) if filters else False
    except:
        selector = False
    else:
        if selector:
            sphinx.SetFilter(filter_name, selector)
            return {field_name: unicode_to_int_list(filters)}
        else:
            return {}


def SetRangeSphinxFilter(sphinx, filter_name, field_name_min, field_name_max, oldform):
    min_value = oldform.cleaned_data[field_name_min]
    max_value = oldform.cleaned_data[field_name_max]
    # Если пустое начальное значение, то выставляем его в 0
    if min_value is None or min_value < 0:
        min_selector = 0
    else:
        min_selector = int(min_value)
    # Если пустое конечное значение, то исключаем все значения меньше начального
    if max_value is None or max_value < 0:
        sphinx.SetFilterRange(filter_name, 0, min_selector, True)
        return {field_name_min: min_selector}
    else:
        max_selector = int(max_value)
        sphinx.SetFilterRange(filter_name, min_selector, max_selector)
        return {field_name_min: min_selector, field_name_max: max_selector}


def SetObjSphinxFilter(sphinx, filter_name, field_name, oldform):
    filters = oldform.cleaned_data[field_name]
    try:
        selector = obj_to_int_list(filters) if filters else False
    except:
        selector = False
    else:
        if selector:
            sphinx.SetFilter(filter_name, selector)
            return {field_name: selector}
        else:
            return {}