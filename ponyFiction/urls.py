# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from ponyFiction.stories import feeds
from ponyFiction.stories.views import search, stories, ajax, chapters, author, comment
from ponyFiction.stories.views.index import index
from ponyFiction.stories.views.stream import stream_list
from django.contrib.auth import views as auth_views
from registration.views import activate, register
from ponyFiction.forms import AuthorRegistrationForm

from ponyFiction.stories.models import Comment, Story, Chapter
from django.views.generic import TemplateView

admin.autodiscover()
random_stories = Story.objects.order_by('?')[0:10]

# Главная страница
urlpatterns = patterns('', url(r'^$', index, {'random_stories': random_stories, 'page_title': 'Главная'}, name='index'))

# Адреса админки
urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))

# Поиск
urlpatterns += patterns('',
                        
    url(r'^search/$',
        search.search_main,
        {
            'random_stories': random_stories,
            'GET': search.search_form,
            'POST': search.search_action,
            'GET_title': 'Поиск историй',
            'POST_title': 'Результаты поиска'
        },
    name='search'),
                        
    url(r'^search/(?P<search_type>\w+)/(?P<search_id>\d+)/$',
        search.search_simple,
        {
            'random_stories': random_stories,
        },
    name='search_simple')
)

# Обработка пользовательских адресов
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/$',
        author.author_info,
        {'random_stories': random_stories, 'page_title': 'Профиль'},
        name='author_overview'),
                        
    url(r'^accounts/profile/$',
        author.author_info,
        {'random_stories': random_stories, 'page_title': 'Мой кабинет'},
        name='author_dashboard'),
                        
    url(r'^accounts/profile/edit/$',
        author.author_edit,
        {'random_stories': random_stories, 'page_title': 'Настройки профиля'},
        name='author_profile_edit'),
                        
    url(r'^accounts/registration/$',
        register,
        {
            'backend': 'registration.backends.pony.PonyBackend',
            'form_class': AuthorRegistrationForm,
            'extra_context': {'random_stories': random_stories, 'page_title': 'Регистрация'}
        },
        name='registration_register'),
    url(r'^accounts/registration/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html',
            get_context_data=lambda: {'random_stories': random_stories, 'page_title': 'Завершение регистрации'},
        ),
        name='registration_complete'),          
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        activate,
        {'backend': 'registration.backends.pony.PonyBackend'},
        name='registration_activate'),
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html',
            get_context_data=lambda: {'random_stories': random_stories, 'page_title': 'Активация'},
        ),
        name='registration_activation_complete'),       
    url(r'^accounts/registration/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html',
            get_context_data=lambda: {'random_stories': random_stories, 'page_title': 'Регистрация закрыта'},
        ),
        name='registration_disallowed'),
    url(r'^accounts/login/$',
        auth_views.login,
        {
            'template_name': 'registration/login.html',
            'extra_context': {'random_stories': random_stories, 'page_title': 'Авторизация'}
        },
        name='auth_login'),
    url(r'^accounts/logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='auth_logout'),
    
)
# Подгрузка комментариев, историй и глав по AJAX
urlpatterns += patterns('',
    url(r'^story/(?P<story_id>\d+)/ajax$', ajax.ajax_comments, {'type' : 'story'}),
    url(r'^accounts/(?P<user_id>\d+)/ajax$', ajax.ajax_comments, {'type' : 'user'}),
    url(r'^stream/comments/ajax$', ajax.ajax_comments, {'type' : 'new'}),
    url(r'^stream/stories/ajax$', ajax.ajax_stories),
    url(r'^stream/chapters/ajax$', ajax.ajax_chapters)
)

# Ленты
urlpatterns += patterns('',

    url(r'^stream/comments/$',
        stream_list,
        {
            'model': Comment,
            'random_stories': random_stories,
            'page_title': 'Лента новых комментариев'
        },
        name='stream_comments'),

    url(r'^stream/stories/$',
        stream_list,
        {
            'model': Story,
            'random_stories': random_stories,
            'page_title': 'Лента новых историй'
        },
        name='stream_stories'),

    url(r'^stream/chapters/$',
        stream_list,
        {
            'model': Chapter,
            'random_stories': random_stories,
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
urlpatterns += patterns('',
    # Просмотр
    url(r'^story/(?P<story_id>\d+)/$',
        stories.story_view,
        {'random_stories': random_stories},
        name='story_view'
    ),
    # Добавление
    url(r'^story/add/$',
        stories.story_work,
        {
            'random_stories': random_stories,
            'page_title': 'Новый рассказ',
        },
        name='story_add'
    ),
    # Правка
    url(r'^story/(?P<story_id>\d+)/edit/$',
        stories.story_work,
        {
         'random_stories': random_stories
        },
        name='story_edit'
    ),
    # AJAX-сортировка глав
    url(r'^story/(?P<story_id>\d+)/edit/ajax$', ajax.sort_chapters),
)

# Работа с главами
urlpatterns += patterns('',
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$', chapters.chapter_view, {'random_stories': random_stories, 'view_type': 'single'}, name='chapter_view_single'),
    url(r'^story/(?P<story_id>\d+)/chapter/all/$', chapters.chapter_view, {'random_stories': random_stories, 'view_type': 'all'}, name='chapter_view_all'),
    # Добавление
    url(r'^story/(?P<story_id>\d+)/chapter/add/$',
        chapters.chapter_work,
        {
            'random_stories': random_stories,
            'page_title': 'Новый рассказ',
        },
        name='chapter_add'
    ),
    # Правка
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/edit/$',
        chapters.chapter_work,
        {
         'random_stories': random_stories
        },
        name='chapter_edit'
    ),
)


urlpatterns += patterns('', 
    url(r'^test_add_chapter/$',
        TemplateView.as_view(
            template_name='add-chapter-pharm.html',
            get_context_data=lambda: {'random_stories': random_stories, 'page_title': 'Добавить главу'},
        ),
    )
)


        
urlpatterns += patterns('ponyFiction.stories.views',  
    url(r'^series/(?P<series_id>\d+)/$', 'series_view')
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )