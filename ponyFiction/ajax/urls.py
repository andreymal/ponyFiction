# -*- coding: utf-8 -*-

from django.conf.urls import url
from ponyFiction.ajax.views import comment, story, chapter

urlpatterns = [
    # Подгрузка комментариев для рассказа
    url(r'story/(?P<story_id>\d+)/comments/page/(?P<page>\d+)/$', comment.CommentsStory.as_view()),
    # Подгрузка комментариев для профиля
    url(r'accounts/(?P<user_id>\d+)/comments/page/(?P<page>\d+)/$', comment.CommentsAuthor.as_view()),
    url(r'accounts/profile/comments/page/(?P<page>\d+)/$', comment.CommentsAuthor.as_view(), {'user_id': None}),

    # Удаление рассказа
    url(r'story/(?P<pk>\d+)/delete/$', story.delete),

    # Одобрение рассказа
    url(r'story/(?P<story_id>\d+)/approve/$', story.story_approve_ajax),
    # Публикация рассказа
    url(r'story/(?P<story_id>\d+)/publish/$', story.story_publish_ajax),
    # Добавление в закладки рассказа
    url(r'story/(?P<story_id>\d+)/bookmark$', story.story_bookmark_ajax),
    # Добавление в избранное рассказа
    url(r'story/(?P<story_id>\d+)/favorite', story.story_favorite_ajax),
    # Добавление в избранное главы (workaround, пока добавляется весь рассказ)
    url(r'story/(?P<story_id>\d+)/chapter/\d+/favorite', story.story_favorite_ajax),
    # Голосование за рассказ
    url(r'story/(?P<story_id>\d+)/vote/(?P<direction>\w+)/$', story.story_vote_ajax),

    # Добавление комментария
    url(r'story/(?P<story_id>\d+)/comment/add/$', comment.AjaxCommentAdd.as_view()),
    # Редактирование комментария
    url(r'story/(?P<story_id>\d+)/comment/(?P<pk>\d+)/edit/$', comment.AjaxCommentEdit.as_view()),
    # Удаление комментария
    url(r'story/(?P<story_id>\d+)/comment/(?P<pk>\d+)/delete/$', comment.AjaxCommentDelete.as_view()),

    # AJAX-сортировка глав
    url(r'story/(?P<story_id>\d+)/sort/$', chapter.chapter_sort),
    # Удаление главы
    url(r'chapter/(?P<pk>\d+)/delete/$', chapter.AjaxChapterDelete.as_view()),
]
