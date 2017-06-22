#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
import django.views.static
from ponyFiction import feeds
from ponyFiction.views import search, author
from ponyFiction.views import story as views_story, chapter as views_chapter, error as views_error, staticpages as views_staticpages
from ponyFiction.views.chapter import ChapterAdd, ChapterEdit, ChapterDelete
from ponyFiction.views.comment import CommentEdit, CommentAdd, CommentDelete
from ponyFiction.views.index import index
from ponyFiction.views.object_lists import FavoritesList, SubmitsList, BookmarksList
from ponyFiction.views.stream import StreamStories, StreamChapters, StreamComments, TopStories, StreamStoryEditLog

from ponyFiction.api import dispatcher
from jsonrpc.backend.django import JSONRPCAPI
api = JSONRPCAPI(dispatcher=dispatcher)

handler403 = 'ponyFiction.views.error.handler403'
handler404 = 'ponyFiction.views.error.handler404'
handler500 = 'ponyFiction.views.error.handler500'


urlpatterns = [
    # Главная страница
    url(r'^$', index, name='index'),
    # Адреса админки
    url(r'^admin/', include(admin.site.urls)),
    # Поиск
    url(r'^search/$', search.search_main, name='search'),
    url(r'^search/(?P<search_type>\w+)/(?P<search_id>\d+)/$', search.search_simple, name='search_simple'),
    # Избранное
    url(r'^accounts/(?P<user_id>\d+)/favorites/$', FavoritesList.as_view(), name='favorites'),
    url(r'^accounts/(?P<user_id>\d+)/favorites/page/(?P<page>\d+)/$', FavoritesList.as_view(), name='favorites_page'),
    # Новые поступления
    url(r'^submitted/$', SubmitsList.as_view(), name='submitted'),
    url(r'^submitted/page/(?P<page>\d+)/$', SubmitsList.as_view(), name='submitted_page'),
    # Закладки
    url(r'^bookmarks/$', BookmarksList.as_view(), name='bookmarks'),
    url(r'^bookmarks/page/(?P<page>\d+)/$', BookmarksList.as_view(), name='bookmarks_page'),
    # Ленты
    url(r'^stream/stories/$', StreamStories.as_view(), name='stream_stories'),
    url(r'^stream/stories/page/(?P<page>\d+)/$', StreamStories.as_view(), name='stream_stories_page'),
    url(r'^stream/chapters/$', StreamChapters.as_view(), name='stream_chapters'),
    url(r'^stream/chapters/page/(?P<page>\d+)/$', StreamChapters.as_view(), name='stream_chapters_page'),
    url(r'^stream/comments/$', StreamComments.as_view(), name='stream_comments'),
    url(r'^stream/comments/page/(?P<page>\d+)/$', StreamComments.as_view(), name='stream_comments_page'),
    url(r'^story/top/(?:page/(?P<page>\d+)/)?$', TopStories.as_view(), name='top_stories'),
    url(r'^stream/editlog/(?:page/(?P<page>\d+|last)/)?$', StreamStoryEditLog.as_view(), name='stream_edit_log'),

    # Обработка пользовательских адресов
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
         'post_reset_redirect': '/accounts/password/reset/done/',
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
         'post_reset_redirect': '/accounts/password/done/',
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

    # AJAX
    url(r'^ajax/', include('ponyFiction.ajax.urls')),

    # Работа с комментариями:
    # Добавление
    url(r'^story/(?P<story_id>\d+)/comment/add/$', CommentAdd.as_view(), name='comment_add'),
    # Редактирование
    url(r'^story/(?P<story_id>\d+)/comment/(?P<pk>\d+)/edit/$', CommentEdit.as_view(), name='comment_edit'),
    # Удаление
    url(r'^story/(?P<story_id>\d+)/comment/(?P<pk>\d+)/delete/$', CommentDelete.as_view(), name='comment_delete'),

    # RSS
    url(r'^feeds/stories/$', feeds.stories(), name='feeds_stories'),
    url(r'^feeds/chapters/$', feeds.chapters(), name='feeds_chapters'),
    url(r'^feeds/story/(?P<story_id>\d+)/$', feeds.story(), name='feeds_story'),

    # Работа с рассказами:
    # Просмотр
    url(r'^story/(?P<pk>\d+)/$', views_story.story_view, {'comments_page': -1}, name='story_view'),
    # Просмотр с подгрузкой определенной страницы комментариев
    url(r'^story/(?P<pk>\d+)/comments/page/(?P<comments_page>\d+)/$', views_story.story_view, name='story_view_comments_paged'),
    # Добавление
    url(r'^story/add/$', views_story.add, name='story_add'),
    # Правка
    url(r'^story/(?P<pk>\d+)/edit/$', views_story.edit, name='story_edit'),
    url(r'^story/(?P<pk>\d+)/delete/$', views_story.delete, name='story_delete'),
    # Отправка на публикацию
    url(r'^story/(?P<pk>\d+)/publish/$', views_story.story_publish, name='story_publish'),
    # Одобрение
    url(r'^story/(?P<pk>\d+)/approve/$', views_story.story_approve, name='story_approve'),
    # Добавление в избранное
    url(r'^story/(?P<pk>\d+)/favorite$', views_story.story_favorite, name='story_favorite'),
    # Добавление в закладки
    url(r'^story/(?P<pk>\d+)/bookmark$', views_story.story_bookmark, name='story_bookmark'),
    # Голосование за рассказ
    url(r'^story/(?P<pk>\d+)/vote/plus/$', views_story.story_vote, {'direction': True}, name='story_vote_plus'),
    url(r'^story/(?P<pk>\d+)/vote/minus/$', views_story.story_vote, {'direction': False}, name='story_vote_minus'),

    url(r'^story/(?P<pk>\d+)/editlog/$', views_story.story_edit_log, name='story_edit_log'),
    # Загрузка рассказа
    url(r'^story/(?P<story_id>\d+)/download/(?P<filename>\w+)\.(?P<extension>[\w\.]+)$', views_story.story_download),

    # Работа с главами
    # Просмотр одной
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$', views_chapter.chapter_view, name='chapter_view_single'),
    # Просмотр всех глав
    url(r'^story/(?P<story_id>\d+)/chapter/all/$', views_chapter.chapter_view, name='chapter_view_all'),
    # Добавление
    url(r'^story/(?P<story_id>\d+)/chapter/add/$', ChapterAdd.as_view(), name='chapter_add'),
    # Правка
    url(r'^chapter/(?P<pk>\d+)/edit/$', ChapterEdit.as_view(), name='chapter_edit'),
    # Удаление
    url(r'^chapter/(?P<pk>\d+)/delete/$', ChapterDelete.as_view(), name='chapter_delete'),

    # Другое
    url(r'^not_found/$', views_error.handler404),
    url(r'^forbidden/$', views_error.handler403),
    url(r'^internal_server_error/$', views_error.handler500),

    url(r'^page/(?P<name>[A-z0-9-_\.]+)/$', views_staticpages.view, name='staticpage'),
]

if settings.DEBUG:
    # Only for debugging purposes, when process runs with "manage.py runserver --nostatic", not with uwsgi+nginx
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': 'media/'}),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns

urlpatterns += [
    url(r'^api/', include(api.urls)),
]
