# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView
from ponyFiction import signals
from ponyFiction.forms.comment import CommentForm
from ponyFiction.forms.story import StoryForm
from ponyFiction.models import Story, CoAuthorsStory, StoryView, Author

@csrf_protect
def story_view(request, pk, comments_page):
    try:
        story = Story.objects.accessible.get(pk=pk)
    except Story.DoesNotExist:
        story = get_object_or_404(Story, pk=pk)
        if not story.editable_by(request.user):
            raise PermissionDenied
    
    chapters = story.chapter_set.order_by('order')
    comments_list = story.comment_set.order_by('-date').all().cache()
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    num_pages = paged.num_pages
    page_current = int(comments_page) if (0 < int(comments_page) <= num_pages) else 1
    comments = paged.page(page_current)
    page_title = story.title
    comment_form = CommentForm()
    signals.story_viewed.send(sender=Author, instance=request.user, story=story, comments_count=comments_list.count())
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
    if (story.editable_by(request.user) and story.publishable):
        if (request.user.approved and not story.approved):
            story.approved = True
        if story.draft:
            story.draft = False
        else:
            story.draft = True
        story.save(update_fields=['draft', 'approved'])
        return redirect('author_dashboard')
    else:
        raise PermissionDenied

@login_required
def story_delete(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.editable_by(request.user):
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
    if story.editable_by(request.user):
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
    initial={'finished': 0, 'freezed': 0, 'original': 1, 'rating': 4, 'button_submit': u'Добавить рассказ'}

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
        if self.story.editable_by(self.request.user):
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

def story_download(request, story_id, filename, extension):
    from django.core.files.storage import default_storage as storage
    from ..downloads import get_format
    
    debug = settings.DEBUG and 'debug' in request.META['QUERY_STRING']
    
    story = get_object_or_404(Story, pk=story_id)
    fmt = get_format(extension)
    if fmt is None:
        raise Http404
    
    url = fmt.url(story)
    if url != request.path:
        return redirect(url)
    filepath = 'downloads/stories/%s/%s.%s' % (story_id, filename, extension)
    
    if (not storage.exists(filepath) or 
        storage.modified_time(filepath) < story.updated or
        debug):
        
        data = fmt.render(
            story = story,
            filename = filename,
            extension = extension,
            debug = debug,
        )
        if not debug:
            storage.save(filepath, ContentFile(data))
        
    if not debug:
        return redirect(storage.url(filepath))
    else:
        response = HttpResponse(data)
        response['Content-Type'] = fmt.debug_content_type
        return response
