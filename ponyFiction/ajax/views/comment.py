# -*- coding: utf-8 -*-
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from ponyFiction.models import Story, Author, Comment
from ponyFiction.ajax.mixins import AJAXHTTPResponseMixin
from ponyFiction.views.comment import CommentAdd, CommentEdit, CommentDelete
from ponyFiction.views.object_lists import ObjectList
from django.utils.decorators import method_decorator
from ponyFiction.ajax.decorators import ajax_required

class AjaxCommentAdd(CommentAdd, AJAXHTTPResponseMixin):

    response_template_name = 'includes/comments.html'

    @property
    def template_name(self):
        return 'includes/ajax/comment_ajax_edit_window.html'

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return CommentAdd.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        parent_response = super(AjaxCommentAdd, self).form_valid(form)
        if parent_response.status_code == 302:
            return render(self.request, self.response_template_name, {'comments': [self.comment]})
        else:
            return parent_response

class AjaxCommentEdit(CommentEdit, AJAXHTTPResponseMixin):

    response_template_name = 'includes/comments.html'

    @property
    def template_name(self):
        return 'includes/ajax/comment_ajax_edit_window.html'

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return CommentEdit.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        parent_response = super(AjaxCommentEdit, self).form_valid(form)
        if parent_response.status_code == 302:
            return render(self.request, self.response_template_name, {'comments': [self.comment], 'story': self.comment.story})
        else:
            return parent_response

class AjaxCommentDelete(CommentDelete):

    template_name = 'includes/ajax/comment_ajax_confirm_delete.html'

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return CommentDelete.dispatch(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        parent_response = super(AjaxCommentDelete, self).delete(self, request, *args, **kwargs)
        if parent_response.status_code == 302:
            return HttpResponse(self.comment_id)
        else:
            return parent_response

class CommentsStory(ObjectList):
    """ Подгрузка комментариев к рассказу"""

    context_object_name = 'comments'
    paginate_by = settings.COMMENTS_COUNT['page']


    @property
    def template_name(self):
        return 'includes/comments.html'

    @property
    def page_title(self):
        return None

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return ObjectList.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        story = get_object_or_404(Story, pk=self.kwargs['story_id'])
        return story.comment_set.order_by('date').cache()

    def get_paginator(self, *a, **kw):
        kw.update(orphans = settings.COMMENTS_ORPHANS)
        return super(CommentsStory, self).get_paginator(*a, **kw)

class CommentsAuthor(ObjectList):
    """ Подгрузка комментариев для профиля """

    context_object_name = 'comments'
    paginate_by = settings.COMMENTS_COUNT['author_page']

    @property
    def template_name(self):
        return 'includes/comments.html'

    @property
    def page_title(self):
        return None

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return ObjectList.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        if self.kwargs['user_id'] is None:
            return Comment.objects.filter(story__authors=self.request.user.id).order_by('-date').cache()
        else:
            author = get_object_or_404(Author, pk=self.kwargs['user_id'])
            return author.comment_set.order_by('-date').cache()
