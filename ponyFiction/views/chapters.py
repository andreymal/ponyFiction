# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Max, F
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from ponyFiction.forms.chapter import ChapterForm
from ponyFiction.models import Story, Chapter, StoryView
from django.views.decorators.csrf import csrf_protect
from cacheops.invalidation import invalidate_obj

def chapter_view(request, story_id=False, chapter_order=False):
    try:
        story = Story.objects.accessible(user=request.user).get(pk=story_id)
    except Story.DoesNotExist:
        story = get_object_or_404(Story, pk=story_id)
        if not story.editable_by(request.user):
            raise PermissionDenied
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
        if request.user.is_authenticated():
            StoryView.objects.create(
                author = request.user,
                story_id = story_id,
                chapter = chapter,
            )
    else:
        chapters = story.chapter_set.order_by('order').cache()
        page_title = story.title+u' – все главы'
        data = {
            'story': story,
            'chapters' : chapters,
            'page_title' : page_title,
            'allchapters': True
        }
        if request.user.is_authenticated():
            StoryView.objects.create(
                author = request.user,
                story_id = story_id,
            )
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

@login_required
@csrf_protect
def chapter_delete(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    story = chapter.story
    if chapter.story.editable_by(request.user):
        story.chapter_set.filter(order__gt=chapter.order).update(order=F('order')-1)
        for ch in story.chapter_set.filter(order__gt=chapter.order):
            invalidate_obj(ch)
        chapter.delete()
        return redirect('story_edit', story.id)
    else:
        raise PermissionDenied