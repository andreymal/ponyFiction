#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from ponyFiction import feeds
from ponyFiction.forms.register import AuthorRegistrationForm
from ponyFiction.views import search, author
from ponyFiction.views.chapter import ChapterAdd, ChapterEdit, ChapterDelete
from ponyFiction.views.comment import CommentEdit, CommentAdd, CommentDelete
from ponyFiction.views.index import index
from ponyFiction.views.object_lists import FavoritesList, SubmitsList, BookmarksList
from ponyFiction.views.story import StoryAdd, StoryEdit, StoryDelete
from ponyFiction.views.stream import StreamStories, StreamChapters, StreamComments, TopStories, StreamStoryEditLog

from ponyFiction.api import dispatcher
from jsonrpc.backend.django import JSONRPCAPI
api = JSONRPCAPI(dispatcher=dispatcher)

admin.autodiscover()

# Главная страница
urlpatterns = patterns('', url(r'^$', index, name='index'))
# Адреса админки
urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))
# Поиск
urlpatterns += patterns('',
    url(r'^search/$', search.search_main, name='search'),
    url(r'^search/(?P<search_type>\w+)/(?P<search_id>\d+)/$', search.search_simple, name='search_simple')
)
# Избранное
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/favorites/$', FavoritesList.as_view(), name='favorites'),
    url(r'^accounts/(?P<user_id>\d+)/favorites/page/(?P<page>\d+)/$', FavoritesList.as_view(), name='favorites_page'),
)
# Новые поступления
urlpatterns += patterns('',
    url(r'^submitted/$', SubmitsList.as_view(), name='submitted'),
    url(r'^submitted/page/(?P<page>\d+)/$', SubmitsList.as_view(), name='submitted_page'),
)
# Закладки
urlpatterns += patterns('',
    url(r'^bookmarks/$', BookmarksList.as_view(), name='bookmarks'),
    url(r'^bookmarks/page/(?P<page>\d+)/$', BookmarksList.as_view(), name='bookmarks_page'),
)
# Ленты
urlpatterns += patterns('',
    url(r'^stream/stories/$', StreamStories.as_view(), name='stream_stories'),
    url(r'^stream/stories/page/(?P<page>\d+)/$', StreamStories.as_view(), name='stream_stories_page'),
    url(r'^stream/chapters/$', StreamChapters.as_view(), name='stream_chapters'),
    url(r'^stream/chapters/page/(?P<page>\d+)/$', StreamChapters.as_view(), name='stream_chapters_page'),
    url(r'^stream/comments/$', StreamComments.as_view(), name='stream_comments'),
    url(r'^stream/comments/page/(?P<page>\d+)/$', StreamComments.as_view(), name='stream_comments_page'),
    url(r'^story/top/(?:page/(?P<page>\d+)/)?$', TopStories.as_view(), name='top_stories'),
    url(r'^stream/editlog/(?:page/(?P<page>\d+|last)/)?$', StreamStoryEditLog.as_view(), name='stream_edit_log'),
)

# Обработка пользовательских адресов
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/$', author.author_info, {'comments_page': 1}, name='author_overview'),
    url(r'^accounts/(?P<user_id>\d+)/comments/page/(?P<comments_page>\d+)/$', author.author_info, name='author_overview_comments_paged'),
    url(r'^accounts/profile/$', author.author_info, {'user_id': None, 'comments_page': 1}, name='author_dashboard'),
    url(r'^accounts/profile/comments/page/(?P<comments_page>\d+)/$', author.author_info, {'user_id': None}, name='author_dashboard_comments_paged'),
    url(r'^accounts/profile/edit/$', author.author_edit, name='author_profile_edit'),
    url(r'^accounts/(?P<user_id>\d+)/approve/$', author.author_approve, name='author_approve'),
    url(r'^accounts/(?P<user_id>\d+)/ban/$', author.author_ban, name='author_ban'),

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
    # Регистрация
    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
        {
         'post_reset_redirect' : '/accounts/password/reset/done/',
         'extra_context': {'page_title': 'Восстановление пароля: введите адрес e-mail'}
         },
        name='password_reset'),
    url(r'^accounts/password/reset/done/$',
        auth_views.password_reset_done,
        {
         'extra_context': {'page_title': 'Восстановление пароля: письмо отправлено'}
         },
        ),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
         'post_reset_redirect' : '/accounts/password/done/',
         'extra_context': {'page_title': 'Восстановление пароля: новый пароль'}
         },
        ),
    url(r'^accounts/password/done/$',
        auth_views.password_reset_complete,
        {
         'extra_context': {'page_title': 'Восстановление пароля: пароль восстановлен'}
         },
        ),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

# stories_migration
if 'stories_migration' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^stories_auth/', include('stories_migration.urls')))

# AJAX
urlpatterns += patterns('', (r'^ajax/', include('ponyFiction.ajax.urls')))

# Работа с комментариями
urlpatterns += patterns('',
    # Добавление
    url(r'^story/(?P<story_id>\d+)/comment/add/$', CommentAdd.as_view(), name='comment_add'),
    # Редактирование
    url(r'^story/(?P<story_id>\d+)/comment/(?P<pk>\d+)/edit/$', CommentEdit.as_view(), name='comment_edit'),
    # Удаление
    url(r'^story/(?P<story_id>\d+)/comment/(?P<pk>\d+)/delete/$', CommentDelete.as_view(), name='comment_delete'),

)

# RSS
urlpatterns += patterns('',
    url(r'^feeds/stories/$', feeds.stories(), name='feeds_stories'),
    url(r'^feeds/chapters/$', feeds.chapters(), name='feeds_chapters'),
    url(r'^feeds/story/(?P<story_id>\d+)/$', feeds.story(), name='feeds_story'),
)

# Работа с рассказами
urlpatterns += patterns('ponyFiction.views.story',
    # Просмотр
    url(r'^story/(?P<pk>\d+)/$', 'story_view', {'comments_page': -1}, name='story_view'),
    # Просмотр с подгрузкой определенной страницы комментариев
    url(r'^story/(?P<pk>\d+)/comments/page/(?P<comments_page>\d+)/$', 'story_view', name='story_view_comments_paged'),
    # Добавление
    url(r'^story/add/$', StoryAdd.as_view(), name='story_add'),
    # Правка
    url(r'^story/(?P<pk>\d+)/edit/$', StoryEdit.as_view(), name='story_edit'),
    url(r'^story/(?P<pk>\d+)/delete/$', StoryDelete.as_view(), name='story_delete'),
    # Отправка на публикацию
    url(r'^story/(?P<pk>\d+)/publish/$', 'story_publish', name='story_publish'),
    # Одобрение
    url(r'^story/(?P<pk>\d+)/approve/$', 'story_approve', name='story_approve'),
    # Добавление в избранное
    url(r'^story/(?P<pk>\d+)/favorite$', 'story_favorite', name='story_favorite'),
    # Добавление в закладки
    url(r'^story/(?P<pk>\d+)/bookmark$', 'story_bookmark', name='story_bookmark'),
    # Голосование за рассказ
    url(r'^story/(?P<pk>\d+)/vote/(?P<value>\d+)/$', 'story_vote', name='story_vote'),

    url(r'^story/(?P<pk>\d+)/editlog/$', 'story_edit_log', name='story_edit_log'),
    # Загрузка рассказа
    url(r'^story/(?P<story_id>\d+)/download/(?P<filename>\w+)\.(?P<extension>[\w\.]+)$', 'story_download'),
)
# Работа с главами
urlpatterns += patterns('ponyFiction.views.chapter',
    # Просмотр одной
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$', 'chapter_view', name='chapter_view_single'),
    # Просмотр всех глав
    url(r'^story/(?P<story_id>\d+)/chapter/all/$', 'chapter_view', name='chapter_view_all'),
    # Добавление
    url(r'^story/(?P<story_id>\d+)/chapter/add/$', ChapterAdd.as_view(), name='chapter_add'),
    # Правка
    url(r'^chapter/(?P<pk>\d+)/edit/$', ChapterEdit.as_view(), name='chapter_edit'),
    # Удаление
    url(r'^chapter/(?P<pk>\d+)/delete/$', ChapterDelete.as_view(), name='chapter_delete'),
)
# Другое
urlpatterns += patterns('',
    url(r'^not_found/$', TemplateView.as_view(template_name='404.html')),
    url(r'^forbidden/$', TemplateView.as_view(template_name='403.html')),
    url(r'^internal_server_error/$', TemplateView.as_view(template_name='500.html')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
urlpatterns += patterns('ponyFiction.views.staticpages',
    url(r'^page/(?P<name>[A-z0-9-_\.]+)/$', 'view', name='staticpage'),
)

urlpatterns += patterns('',
    url(r'^api/', include(api.urls)),
)
