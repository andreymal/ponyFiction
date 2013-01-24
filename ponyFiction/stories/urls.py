# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
# Работа с историями
urlpatterns = patterns('ponyFiction.stories.views.stories',
    # Просмотр
    url(r'(?P<story_id>\d+)/$',
        'story_view', name='story_view'
    ),
    # Добавление
    url(r'add/$',
        'story_work', name='story_add'
    ),
    # Правка
    url(r'(?P<story_id>\d+)/edit/$',
        'story_work', name='story_edit'
    ),
)
# Работа с главами
urlpatterns += patterns('ponyFiction.stories.views.chapters',
    # Просмотр одной
    url(r'(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$',
        'chapter_view_single', name='chapter_view_single'
    ),
    # Просмотр всех глав
    url(r'(?P<story_id>\d+)/chapter/all/$',
        'chapter_view_all', name='chapter_view_all'
    ),
    # Добавление
    url(r'(?P<story_id>\d+)/chapter/add/$',
        'chapter_work', name='chapter_add'
    ),
    # Правка
    url(r'(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/edit/$',
        'chapter_work', name='chapter_edit'
    ),
)