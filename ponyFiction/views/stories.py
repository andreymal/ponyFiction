# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView
from ponyFiction.forms.comment import CommentForm
from ponyFiction.forms.story import StoryForm
from ponyFiction.models import Story, CoAuthorsStory, StoryView, Activity

@csrf_protect
def story_view(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    chapters = story.chapter_set.order_by('order')
    comments_list = story.comment_set.all()
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    num_pages = paged.num_pages
    comments = paged.page(1)
    page_title = story.title
    comment_form = CommentForm()
    if request.user.is_authenticated():
        activity = Activity.objects.get_or_create(author_id=request.user.id, story=story)[0]
        activity.last_views = story.views()
        activity.last_comments = comments_list.count()
        activity.last_vote_up = story.vote_up_count()
        activity.last_vote_down = story.vote_down_count()
        activity.save()
    data = {
       'story' : story,
       'comments' : comments,
       'chapters' : chapters,
       'num_pages' : num_pages,
       'page_title' : page_title,
       'comment_form': comment_form
       }
    # Если только одна глава
    if (story.chapter_set.count() == 1 and request.user.is_authenticated()):
        view = StoryView.objects.create()
        view.author = request.user
        view.story_id = story_id
        view.chapter = story.chapter_set.all()[0]
        view.save()
    return render(request, 'story_view.html', data)

@login_required
@csrf_protect
def story_delete(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.is_editable_by(request.user) and request.user.is_staff:
        if story.approved:
            story.approved = False
        else:
            story.approved = True
        story.save(update_fields=['approved'])
        return redirect('author_dashboard')
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_publish(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.is_editable_by(request.user):
        if story.draft:
            story.draft = False
        else:
            story.draft = True
        story.save(update_fields=['draft'])
        return redirect('author_dashboard')
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_approve(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.is_editable_by(request.user):
        story.delete()
        return redirect('submitted')
    else:
        raise PermissionDenied
    
class StoryAdd(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_work.html'
    initial={'finished': 0, 'freezed': 0, 'original': 1, 'rating': 4, 'size': 1, 'button_submit': u'Добавить рассказ'}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return CreateView.dispatch(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        story = form.save()
        CoAuthorsStory.objects.create(story = story, author = self.request.user, approved = True)
        return redirect('story_edit', story.id)
    
    def get_context_data(self, **kwargs):
        context = super(StoryAdd, self).get_context_data(**kwargs)
        extra_context = {'page_title': u'Новый рассказ'}
        context.update(extra_context)
        return context


class StoryEdit(UpdateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_work.html'
    initial={'button_submit': u'Сохранить изменения'}
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return UpdateView.dispatch(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        story = form.save()
        return redirect('story_edit', story.id)
    
    def get_context_data(self, **kwargs):
        context = super(StoryEdit, self).get_context_data(**kwargs)
        extra_context = {
                         'page_title': u'Редактирование «%s»' % context['story'].title,
                         'story_edit': True,
                         'chapters': context['story'].chapter_set.order_by('order')
                         }
        context.update(extra_context)
        return context