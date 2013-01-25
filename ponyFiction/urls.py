# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from ponyFiction.stories import feeds
from ponyFiction.stories.views import search, ajax, author, comment
from ponyFiction.stories.views.index import index
from ponyFiction.stories.views.stream import stream_list
from django.contrib.auth import views as auth_views
from registration.views import activate, register
from ponyFiction.stories.forms.register import AuthorRegistrationForm

from ponyFiction.stories.models import Comment, Story, Chapter
from django.views.generic import TemplateView

admin.autodiscover()

# Главная страница
urlpatterns = patterns('', url(r'^$', index, {'page_title': 'Главная'}, name='index'))

# Адреса админки
urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))

# Поиск
urlpatterns += patterns('',
    url(r'^search/$', search.search_main, name='search'),
    url(r'^search/(?P<search_type>\w+)/(?P<search_id>\d+)/$', search.search_simple, name='search_simple')
)

# Обработка пользовательских адресов
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/$',
        author.author_info,
        {'page_title': 'Профиль'},
        name='author_overview'),
                        
    url(r'^accounts/profile/$',
        author.author_info,
        {'page_title': 'Мой кабинет'},
        name='author_dashboard'),
                        
    url(r'^accounts/profile/edit/$',
        author.author_edit,
        {'page_title': 'Настройки профиля'},
        name='author_profile_edit'),
                        
    url(r'^accounts/registration/$',
        register,
        {
            'backend': 'registration.backends.pony.PonyBackend',
            'form_class': AuthorRegistrationForm,
            'extra_context': {'page_title': 'Регистрация'}
        },
        name='registration_register'),
    url(r'^accounts/registration/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html',
            get_context_data=lambda: {'page_title': 'Завершение регистрации'},
        ),
        name='registration_complete'),          
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        activate,
        {'backend': 'registration.backends.pony.PonyBackend'},
        name='registration_activate'),
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html',
            get_context_data=lambda: {'page_title': 'Активация'},
        ),
        name='registration_activation_complete'),       
    url(r'^accounts/registration/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html',
            get_context_data=lambda: {'page_title': 'Регистрация закрыта'},
        ),
        name='registration_disallowed'),
    url(r'^accounts/login/$',
        auth_views.login,
        {
            'template_name': 'registration/login.html',
            'extra_context': {'page_title': 'Авторизация'}
        },
        name='auth_login'),
    url(r'^accounts/logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='auth_logout'),
    
)
# AJAX
urlpatterns += patterns('',
    url(r'^story/(?P<story_id>\d+)/ajax$', ajax.ajax_comments, {'type' : 'story'}),
    url(r'^accounts/(?P<user_id>\d+)/ajax$', ajax.ajax_comments, {'type' : 'user'}),
    url(r'^stream/comments/ajax$', ajax.ajax_comments, {'type' : 'new'}),
    url(r'^stream/stories/ajax$', ajax.ajax_stories),
    url(r'^stream/chapters/ajax$', ajax.ajax_chapters),
    # AJAX-сортировка глав
    url(r'^story/(?P<story_id>\d+)/edit/ajax$', ajax.sort_chapters),
    # Голосование за историю
    url(r'^story/(?P<story_id>\d+)/vote$', ajax.story_vote, name='story_vote'),
)

# Ленты
urlpatterns += patterns('',

    url(r'^stream/comments/$',
        stream_list,
        {
            'model': Comment,
            'page_title': 'Лента новых комментариев'
        },
        name='stream_comments'),

    url(r'^stream/stories/$',
        stream_list,
        {
            'model': Story,
            'page_title': 'Лента новых историй'
        },
        name='stream_stories'),

    url(r'^stream/chapters/$',
        stream_list,
        {
            'model': Chapter,
            'page_title': 'Лента новых глав'
        },
        name='stream_chapters'),
)

# Комментирование
urlpatterns += patterns('',
    url(r'^story/(?P<story_id>\d+)/comment$', comment.comment_story, name='comment_story'),
)

# RSS
urlpatterns += patterns('', 
    url(r'^feeds/rss/stories/$', feeds.stories_rss(), name='feeds_rss_stories'),
    url(r'^feeds/atom/stories/$', feeds.stories_atom(), name='feeds_atom_stories'),
    url(r'^feeds/rss/chapters/$', feeds.chapters_rss(), name='feeds_rss_chapters'),
    url(r'^feeds/atom/chapters/$', feeds.chapters_atom(), name='feeds_atom_chapters'),
    url(r'^feeds/rss/story/(?P<story_id>\d+)/$', feeds.story_chapters_rss(), name='feeds_rss_story'),
    url(r'^feeds/atom/story/(?P<story_id>\d+)/$', feeds.story_chapters_atom(), name='feeds_atom_story'),
)

# Работа с историями
urlpatterns += patterns('ponyFiction.stories.views.stories',
    # Просмотр
    url(r'^story/(?P<story_id>\d+)/$',
        'story_view', name='story_view'
    ),
    # Добавление
    url(r'^story/add/$',
        'story_work', name='story_add'
    ),
    # Правка
    url(r'^story/(?P<story_id>\d+)/edit/$',
        'story_work', name='story_edit'
    ),
)
# Работа с главами
urlpatterns += patterns('ponyFiction.stories.views.chapters',
    # Просмотр одной
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$',
        'chapter_view', name='chapter_view_single'
    ),
    # Просмотр всех глав
    url(r'^story/(?P<story_id>\d+)/chapter/all/$',
        'chapter_view', name='chapter_view_all'
    ),
    # Добавление
    url(r'^story/(?P<story_id>\d+)/chapter/add/$',
        'chapter_work', name='chapter_add'
    ),
    # Правка
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/edit/$',
        'chapter_work', name='chapter_edit'
    ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )