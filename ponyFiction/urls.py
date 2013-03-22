# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from ponyFiction import feeds
from ponyFiction.forms.register import AuthorRegistrationForm
from ponyFiction.views import search, ajax, author, comment, DirectTemplateView # TODO: заменить на это! 
from ponyFiction.views.index import index
from ponyFiction.views.object_lists import FavoritesList, SubmitsList, DeferredStoriesList
from ponyFiction.views.stream import StreamStories, StreamChapters, StreamComments
from registration.views import activate, register
from ponyFiction.views.stories import CommentsStory

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
    url(r'^deferred/$', DeferredStoriesList.as_view(), name='deferred'),
    url(r'^deferred/page/(?P<page>\d+)/$', DeferredStoriesList.as_view(), name='deferred_page'),
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
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/ajax/comments/page/(?P<page>\d+)/$', author.CommentsAuthor.as_view()),
    url(r'^accounts/profile/ajax/comments/page/(?P<page>\d+)/$', author.CommentsAuthor.as_view(), {'user_id': None}),
)        

# Обработка пользовательских адресов
urlpatterns += patterns('',
    url(r'^accounts/(?P<user_id>\d+)/$', author.author_info, name='author_overview'),
    url(r'^accounts/profile/$', author.author_info, name='author_dashboard'),
    url(r'^accounts/profile/edit/$', author.author_edit, name='author_profile_edit'),
    
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
    url(r'^story/(?P<story_id>\d+)/ajax/comments/page/(?P<page>\d+)/$', CommentsStory.as_view()),
    
    # AJAX-сортировка глав
    url(r'^story/(?P<story_id>\d+)/edit/ajax$', ajax.sort_chapters),
    # Голосование за рассказ
    url(r'^story/(?P<story_id>\d+)/vote$', ajax.story_vote, name='story_vote'),
    # Добавление в избранное рассказа
    url(r'^story/(?P<story_id>\d+)/favorite$', ajax.favorites_work, name='favorites_work'),
    # Добавление в избранное главы (workaround, пока добавляется весь рассказ)
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_id>\d+)/favorite$', ajax.favorites_work, name='favorites_work'),

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

# Работа с рассказами
urlpatterns += patterns('ponyFiction.views.stories',
    # Просмотр
    url(r'^story/(?P<story_id>\d+)/$', 'story_view', name='story_view'),
    # Добавление
    url(r'^story/add/$', 'story_work', name='story_add'),
    # Правка
    url(r'^story/(?P<story_id>\d+)/edit/$', 'story_work', {'edit': True}, name='story_edit'),
    # Отправка на публикацию
    url(r'^story/(?P<story_id>\d+)/publish/$', 'story_work', {'publish': True}, name='story_publish'),
    # Одобрение
    url(r'^story/(?P<story_id>\d+)/approve/$', 'story_work', {'approve': True}, name='story_approve'),
    # Удаление
    url(r'^story/(?P<story_id>\d+)/delete/$', 'story_work', {'delete': True}, name='story_delete'),
)
# Работа с главами
urlpatterns += patterns('ponyFiction.views.chapters',
    # Просмотр одной
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_order>\d+)/$','chapter_view', name='chapter_view_single'),
    # Просмотр всех глав
    url(r'^story/(?P<story_id>\d+)/chapter/all/$', 'chapter_view', name='chapter_view_all'),
    # Добавление
    url(r'^story/(?P<story_id>\d+)/chapter/add/$', 'chapter_work', name='chapter_add'),
    # Правка
    url(r'^story/(?P<story_id>\d+)/chapter/(?P<chapter_id>\d+)/edit/$', 'chapter_work', name='chapter_edit'),
)

# Другое
urlpatterns += patterns('',
    url(r'^not_found/$', DirectTemplateView.as_view(template_name='404.html')),
    url(r'^bad_gateway/$', TemplateView.as_view(template_name='502.html')),
    url(r'^forbidden/$', TemplateView.as_view(template_name='403.html')),
    url(r'^internal_server_error/$', TemplateView.as_view(template_name='500.html')),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html', get_context_data=lambda: {'page_title': 'FAQ'}), name='faq'),
    url(r'^terms/$', TemplateView.as_view(template_name='terms.html', get_context_data=lambda: {'page_title': 'Правила'}), name='terms'),
    url(r'^help/$', TemplateView.as_view(template_name='help.html', get_context_data=lambda: {'page_title': 'Помощь'}), name='help'),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )