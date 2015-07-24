# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ponyFiction.forms.comment import CommentForm
from ponyFiction.models import Story, Comment

class CommentAdd(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_work.html'
    initial={'button_submit': u'Добавить'}
    comment = None
    story = None
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        self.story = get_object_or_404(Story.objects.accessible(user=request.user), pk=kwargs['story_id'])
        return CreateView.dispatch(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.story = self.story
        comment.author = self.request.user
        comment.ip = self.request.META['REMOTE_ADDR']
        comment.save()
        self.comment = comment
        return redirect('story_view', self.kwargs['story_id'])
    
    def get_context_data(self, **kwargs):
        context = super(CommentAdd, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Добавить новый комментарий', 'story': self.story, 'edit': False}
        context.update(extra_context)
        return context
    
class CommentEdit(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_work.html'
    initial={'button_submit': u'Сохранить изменения'}
    comment = None
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return UpdateView.dispatch(self, request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.comment = UpdateView.get_object(self, queryset=queryset)
        if self.comment.editable_by(self.request.user):
            return self.comment
        else:
            raise PermissionDenied
    
    def form_valid(self, form):
        self.comment = form.save()
        return redirect('story_view', self.comment.story.id)

    def get_context_data(self, **kwargs):
        context = super(CommentEdit, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Редактировать комментарий', 'story': self.comment.story, 'comment': self.comment, 'edit': True}
        context.update(extra_context)
        return context

class CommentDelete(DeleteView):
    model = Comment
    comment = None
    template_name = 'comment_confirm_delete.html'
    comment_id = None
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return DeleteView.dispatch(self, request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.comment = DeleteView.get_object(self, queryset=queryset)
        self.comment_id = self.comment.id
        if self.comment.editable_by(self.request.user):
            return self.comment
        else:
            raise PermissionDenied
        
    def delete(self, request, *args, **kwargs):
        self.comment = self.get_object()
        self.comment.delete()
        return redirect('story_view', self.kwargs['story_id'])
            
    def get_context_data(self, **kwargs):
        context = super(CommentDelete, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Подтверждение удаления комментария', 'story': self.comment.story}
        context.update(extra_context)
        return context
