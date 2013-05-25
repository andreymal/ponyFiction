# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Max, F
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ponyFiction import signals
from ponyFiction.forms.chapter import ChapterForm
from ponyFiction.models import Story, Chapter, Author
from django.views.decorators.csrf import csrf_protect
from cacheops.invalidation import invalidate_obj

def chapter_view(request, story_id=False, chapter_order=False):
    try:
        story = Story.objects.accessible(user=request.user).get(pk=story_id)
    except Story.DoesNotExist:
        story = get_object_or_404(Story, pk=story_id)
        if not story.editable_by(request.user):
            raise PermissionDenied
    comments_list = story.comment_set.order_by('-date').all().cache()
    signals.story_viewed.send(sender=Author, instance=request.user, story=story, comments_count=comments_list.count())
    if chapter_order:
        chapter = get_object_or_404(story.chapter_set, order=chapter_order)
        page_title = chapter.title[0:80]+' : '+chapter.story.title
        prev_chapter = chapter.get_prev_chapter()
        next_chapter = chapter.get_next_chapter()
        data = {
           'story': story,
           'chapter' : chapter,
           'prev_chapter' : prev_chapter,
           'next_chapter' : next_chapter,
           'page_title' : page_title,
           'allchapters': False
        }
    else:
        chapters = story.chapter_set.order_by('order').cache()
        page_title = story.title+u' – все главы'
        data = {
            'story': story,
            'chapters' : chapters,
            'page_title' : page_title,
            'allchapters': True
        }
    return render(request, 'chapter_view.html', data) 

class ChapterAdd(CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'chapter_work.html'
    initial={'button_submit': u'Добавить'}
    story = None
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        self.story = get_object_or_404(Story, pk=kwargs['story_id'])
        if self.story.editable_by(request.user):
            return CreateView.dispatch(self, request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def form_valid(self, form):
        chapter = form.save(commit=False)
        chapter.story = self.story
        chapter.order = (self.story.chapter_set.aggregate(o=Max('order'))['o'] or 0) + 1
        chapter.save()
        return redirect('chapter_edit', chapter.id)
    
    def get_context_data(self, **kwargs):
        context = super(ChapterAdd, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Добавить новую главу', 'story': self.story}
        context.update(extra_context)
        return context

class ChapterEdit(UpdateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'chapter_work.html'
    initial={'button_submit': u'Сохранить изменения'}
    chapter = None
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return UpdateView.dispatch(self, request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.chapter = UpdateView.get_object(self, queryset=queryset)
        if self.chapter.story.editable_by(self.request.user):
            return self.chapter
        else:
            raise PermissionDenied
    
    def form_valid(self, form):
        self.chapter = form.save()
        return redirect('chapter_edit', self.chapter.id)

    def get_context_data(self, **kwargs):
        context = super(ChapterEdit, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Редактирование «%s»' % self.chapter.title, 'chapter': self.chapter}
        context.update(extra_context)
        return context


class ChapterDelete(DeleteView):
    model = Chapter
    chapter = None
    story = None
    chapter_id = None
    template_name = 'chapter_confirm_delete.html'
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return DeleteView.dispatch(self, request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        self.chapter = DeleteView.get_object(self, queryset=queryset)
        self.story = self.chapter.story
        self.chapter_id = self.chapter.id
        if self.story.editable_by(self.request.user):
            return self.chapter
        else:
            raise PermissionDenied
    
    def delete(self, request, *args, **kwargs):
        self.chapter = self.get_object()
        self.story.chapter_set.filter(order__gt=self.chapter.order).update(order=F('order')-1)
        for chapter in self.story.chapter_set.filter(order__gt=self.chapter.order):
            invalidate_obj(chapter)
        self.chapter.delete()
        return redirect('story_edit', self.story.id)
    
    def get_context_data(self, **kwargs):
        context = super(ChapterDelete, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Подтверждение удаления главы', 'story': self.story, 'chapter': self.chapter}
        context.update(extra_context)
        return context