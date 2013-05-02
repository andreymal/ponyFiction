# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from ponyFiction import feeds
from ponyFiction.forms.register import AuthorRegistrationForm
from ponyFiction.views import search, ajax, author, comment
from ponyFiction.views.index import index
from ponyFiction.views.object_lists import FavoritesList, SubmitsList, BookmarksList
from ponyFiction.views.stream import StreamStories, StreamChapters, StreamComments
from registration.views import activate, register
from ponyFiction.views.stories import StoryAdd, StoryEdit
from ponyFiction.views.chapters import ChapterAdd, ChapterEdit
from ponyFiction.views.comment import CommentEdit, CommentAdd, CommentDelete

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
)
    

# Обработка пользовательских адресов
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/$', author.author_info, {'comments_page': 1}, name='author_overview'),
    url(r'^accounts/(?P<user_id>\d+)/comments/page/(?P<comments_page>\d+)/$', author.author_info, name='author_overview_comments_paged'),
    url(r'^accounts/profile/$', author.author_info, {'user_id': None, 'comments_page': 1}, name='author_dashboard'),
    url(r'^accounts/profile/comments/page/(?P<comments_page>\d+)/$', author.author_info, name='author_dashboard_comments_paged'),
    url(r'^accounts/profile/edit/$', author.author_edit, name='author_profile_edit'),
    url(r'^accounts/(?P<user_id>\d+)/approve/$', author.author_approve, name='author_approve'),

    url(r'^accounts/registration/$',
        register,
        {
            'backend': 'registration.backends.default.DefaultBackend',
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
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html',
            get_context_data=lambda: {'page_title': 'Активация'},
        ),
        name='registration_activation_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        activate,
        {
            'backend': 'registration.backends.default.DefaultBackend',
            'template_name': 'registration/activate.html',
            'success_url' : '/accounts/activate/complete/'
        },
        name='registration_activate'),
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
)
# AJAX
urlpatterns += patterns('',
    # Подгрузка комментариев для рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/comments/page/(?P<page>\d+)/$', ajax.CommentsStory.as_view()),
    # Подгрузка комментариев для профиля
    url(r'^ajax/accounts/(?P<user_id>\d+)/comments/page/(?P<page>\d+)/$', ajax.CommentsAuthor.as_view()),
    url(r'^ajax/accounts/profile/comments/page/(?P<page>\d+)/$', ajax.CommentsAuthor.as_view(), {'user_id': None}),
    # Загрузка модального окна-подтверждения удаления рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/delete/confirm/$', ajax.ConfirmDeleteStory.as_view()),
    # Удаление рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/delete/$', ajax.story_delete_ajax),
    # Одобрение рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/approve/$', ajax.story_approve_ajax),
    # Публикация рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/publish/$', ajax.story_publish_ajax),
    # Добавление в закладки рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/bookmark$', ajax.story_bookmark_ajax),
    # Добавление в избранное рассказа
    url(r'^ajax/story/(?P<story_id>\d+)/favorite', ajax.story_favorite_ajax),
    # Добавление в избранное главы (workaround, пока добавляется весь рассказ)
    url(r'^ajax/story/(?P<story_id>\d+)/chapter/\d+/favorite', ajax.story_favorite_ajax),
    # Голосование за рассказ
    url(r'^ajax/story/(?P<story_id>\d+)/vote/(?P<direction>\w+)/$', ajax.story_vote_ajax),
    # Одобрение автора
    url(r'^ajax/accounts/(?P<user_id>\d+)/approve/$', ajax.author_approve_ajax),
    # Загрузка модального окна-подтверждения удаления главы
    url(r'^ajax/chapter/(?P<chapter_id>\d+)/delete/confirm/$', ajax.ConfirmDeleteChapter.as_view()),
    # Удаление главы
    url(r'^ajax/chapter/(?P<chapter_id>\d+)/delete/$', ajax.chapter_delete_ajax),
    
    # AJAX-сортировка глав
    url(r'^story/(?P<story_id>\d+)/edit/ajax$', ajax.chapter_sort),
)

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
urlpatterns += patterns('ponyFiction.views.stories',
    # Просмотр
    url(r'^story/(?P<pk>\d+)/$', 'story_view', {'comments_page': 1}, name='story_view'),
    # Просмотр с подгрузкой определенной страницы комментариев
    url(r'^story/(?P<pk>\d+)/comments/page/(?P<comments_page>\d+)/$', 'story_view', name='story_view_comments_paged'),
    # Добавление
    url(r'^story/add/$', StoryAdd.as_view(), name='story_add'),
    # Правка
    url(r'^story/(?P<pk>\d+)/edit/$', StoryEdit.as_view(), name='story_edit'),
    # Удаление
    url(r'^story/(?P<pk>\d+)/delete/$', 'story_delete', name='story_delete'),
    # Отправка на публикацию
    url(r'^story/(?P<pk>\d+)/publish/$', 'story_publish', name='story_publish'),
    # Одобрение
    url(r'^story/(?P<pk>\d+)/approve/$', 'story_approve', name='story_approve'),
    # Добавление в избранное
    url(r'^story/(?P<pk>\d+)/favorite$', 'story_favorite', name='story_favorite'),
    # Добавление в закладки
    url(r'^story/(?P<pk>\d+)/bookmark$', 'story_bookmark', name='story_bookmark'),
    # Голосование за рассказ
    url(r'^story/(?P<pk>\d+)/vote/plus/$', 'story_vote', {'direction': True}, name='story_vote_plus'),
    url(r'^story/(?P<pk>\d+)/vote/minus/$', 'story_vote', {'direction': False}, name='story_vote_minus'),
    # Загрузка рассказа
    url(r'^story/(?P<story_id>\d+)/download/(?P<filename>\w+)\.(?P<extension>[\w\.]+)$', 'story_download'),
)
# Работа с главами
urlpatterns += patterns('ponyFiction.views.chapters',
    # Просмотр одной
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$','chapter_view', name='chapter_view_single'),
    # Просмотр всех глав
    url(r'^shtory/(?P<story_id>\d+)/chapter/all/$', 'chapter_view', name='chapter_view_all'),
    # Добавление
    url(r'^story/(?P<story_id>\d+)/chapter/add/$', ChapterAdd.as_view(), name='chapter_add'),
    # Правка
    url(r'^chapter/(?P<pk>\d+)/edit/$', ChapterEdit.as_view(), name='chapter_edit'),
    # Удаление
    url(r'^chapter/(?P<pk>\d+)/delete/$', 'chapter_delete', name='chapter_delete'),
)


# Другое
urlpatterns += patterns('',
    url(r'^not_found/$', TemplateView.as_view(template_name='404.html')),
    url(r'^bad_gateway/$', TemplateView.as_view(template_name='502.html')),
    url(r'^forbidden/$', TemplateView.as_view(template_name='403.html')),
    url(r'^internal_server_error/$', TemplateView.as_view(template_name='500.html')),
    url(r'^terms/$', TemplateView.as_view(template_name='terms.html', get_context_data=lambda: {'page_title': 'Правила'}), name='terms'),
    url(r'^help/$', TemplateView.as_view(template_name='help.html', get_context_data=lambda: {'page_title': 'Справка'}), name='help'),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )