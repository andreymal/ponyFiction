# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView
from ponyFiction.forms.comment import CommentForm
from ponyFiction.forms.story import StoryForm
from ponyFiction.models import Story, CoAuthorsStory, StoryView, Activity

@csrf_protect
def story_view(request, pk, comments_page):
    try:
        story = Story.objects.accessible.get(pk=pk)
    except Story.DoesNotExist:
        story = get_object_or_404(Story, pk=pk)
        if not story.is_editable_by(request.user):
            raise PermissionDenied
    
    chapters = story.chapter_set.order_by('order')
    comments_list = story.comment_set.all()
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    num_pages = paged.num_pages
    page_current = int(comments_page) if (0 < int(comments_page) <= num_pages) else 1
    comments = paged.page(page_current)
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
       'page_current' : page_current,
       'page_title' : page_title,
       'comment_form': comment_form
       }
    # Если только одна глава
    if (story.chapter_set.count() == 1 and request.user.is_authenticated()):
        view = StoryView.objects.create()
        view.author = request.user
        view.story_id = pk
        view.chapter = story.chapter_set.all()[0]
        view.save()
    return render(request, 'story_view.html', data)

@login_required
@csrf_protect
def story_approve(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user.is_staff:
        if story.approved:
            story.approved = False
        else:
            story.approved = True
        story.save(update_fields=['approved'])
        return redirect('submitted')
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
def story_delete(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.is_editable_by(request.user):
        story.delete()
        return redirect('index')
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_favorite(request, pk):
    from ponyFiction.models import Favorites
    story = get_object_or_404(Story.objects.published, pk=pk)
    (favorite, created) = Favorites.objects.get_or_create(story=story, author=request.user)
    if not created:
        favorite.delete()
    return redirect('favorites', request.user.id)

@login_required
@csrf_protect
def story_bookmark(request, pk):
    from ponyFiction.models import Bookmark
    story = get_object_or_404(Story.objects.published, pk=pk)
    (bookmark, created) = Bookmark.objects.get_or_create(story=story, author=request.user)
    if not created:
        bookmark.delete()
    return redirect('bookmarks')

@login_required
@csrf_protect
def story_vote(request, pk, direction):
    story = get_object_or_404(Story.objects.published, pk=pk)
    if story.is_editable_by(request.user):
        redirect('story_view', pk)
    vote = story.vote.get_or_create(author=request.user)[0]
    if direction:
        vote.plus = True
        vote.minus = None
    else:
        vote.plus = None
        vote.minus = True
    vote.save(update_fields=['plus', 'minus'])
    story.vote.add(vote)
    return redirect('story_view', pk)

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
        if self.request.user.approved:
            story.approved = True
            story.save(update_fields=['approved'])
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
    story = None
    
    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return UpdateView.dispatch(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        story = form.save()
        return redirect('story_edit', story.id)
    
    def get_object(self, queryset=None):
        self.story = UpdateView.get_object(self, queryset=queryset)
        if self.story.is_editable_by(self.request.user):
            return self.story
        else:
            raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        context = super(StoryEdit, self).get_context_data(**kwargs)
        extra_context = {
                         'page_title': u'Редактирование «%s»' % self.story.title,
                         'story_edit': True,
                         'chapters': self.story.chapter_set.order_by('order')
                         }
        context.update(extra_context)
        return context

@cache_page(60 * 60 * 24)
def story_fb2(request, pk):
    from lxml import etree
    from ponyFiction.filters import fb2
    story = get_object_or_404(Story, pk=pk)
    chapters = story.chapter_set.order_by('order')
    chapters = [fb2.html_to_fb2(chapter.text_as_html, title = chapter.title) for chapter in chapters]
    doc = fb2.join_fb2_docs(chapters, title = story.title)
    data = etree.tostring(doc, encoding = 'utf8', xml_declaration = True)
    response = HttpResponse(data, content_type = 'text/xml')
    response['Content-Disposition'] = 'attachment; filename=%s.fb2' % pk
    return response

@cache_page(60 * 60 * 24)
def story_html(request, pk):
    story = get_object_or_404(Story, pk=pk)
    data = {'story': story}
    response = render(request, 'clear_html.html', data)
    response['Content-Disposition'] = 'attachment; filename=%s.html' % pk
    return response