# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from ponyFiction import signals
from ponyFiction.forms.comment import CommentForm
from ponyFiction.forms.story import StoryForm
from ponyFiction.models import Story, Author
from cacheops import invalidate_obj
from ponyFiction.utils.misc import get_object_or_none


def get_story(request, pk):
    try:
        story = Story.objects.prefetch_related('authors', 'characters', 'categories', 'classifications').accessible(user=request.user).get(pk=pk)
    except Story.DoesNotExist:
        story = get_object_or_404(Story, pk=pk)
        if not story.editable_by(request.user):
            raise PermissionDenied
    return story


def story_view(request, pk, comments_page):
    story = get_story(request, pk)
    chapters = story.chapter_set.only('title', 'words', 'order').order_by('order')
    comments_list = story.comment_set.order_by('date', 'id').all().prefetch_related('author')
    comments_count = comments_list.count()
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    num_pages = paged.num_pages
    page_current = int(comments_page) if (0 < int(comments_page) <= num_pages) else num_pages
    comments = paged.page(page_current)
    page_title = story.title
    comment_form = CommentForm()
    if request.user.is_authenticated:
        signals.story_visited.send(sender=Author, instance=request.user, story=story, comments_count=comments_list.count())
        if story.chapter_set.count() == 1:
            signals.story_viewed.send(sender=Author, instance=request.user, story=story, chapter=story.chapter_set.all()[0])
        vote = get_object_or_none(story.vote, author=request.user)
    else:
        vote = None

    data = {
       'story': story,
       'vote': vote,
       'comments': comments,
       'comments_count': comments_count,
       'chapters': chapters,
       'num_pages': num_pages,
       'page_current': page_current,
       'page_title': page_title,
       'comment_form': comment_form
       }

    return render(request, 'story_view.html', data)


@login_required
@csrf_protect
@require_POST
def story_approve(request, pk):
    raise PermissionDenied


@login_required
@csrf_protect
def story_publish_warning(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.editable_by(request.user) or request.user.is_staff:
        data = {
                'page_title': 'Неудачная попытка публикации',
                'story': story
                }
        return render(request, 'story_publish_warning.html', data)
    else:
        raise PermissionDenied


@login_required
@csrf_protect
@require_POST
def story_publish(request, pk):
    raise PermissionDenied


@login_required
@csrf_protect
@require_POST
def story_favorite(request, pk):
    from ponyFiction.models import Favorites
    story = get_object_or_404(Story.objects.accessible(user=request.user), pk=pk)
    (favorite, created) = Favorites.objects.get_or_create(story=story, author=request.user)
    if not created:
        favorite.delete()
    invalidate_obj(story)
    return redirect('favorites', request.user.id)


@login_required
@csrf_protect
@require_POST
def story_bookmark(request, pk):
    from ponyFiction.models import Bookmark
    story = get_object_or_404(Story.objects.accessible(user=request.user), pk=pk)
    (bookmark, created) = Bookmark.objects.get_or_create(story=story, author=request.user)
    if not created:
        bookmark.delete()
    invalidate_obj(story)
    return redirect('bookmarks')


@login_required
@csrf_protect
@require_POST
def _story_vote(request, pk, direction):
    story = get_object_or_404(Story.objects.accessible(user=request.user), pk=pk)
    if story.is_author(request.user):
        return story
    vote = story.vote.get_or_create(author=request.user)[0]
    vote.plus = direction
    vote.minus = not direction
    vote.ip = request.META['REMOTE_ADDR']
    vote.save()
    return story


def story_vote(request, pk, direction):
    _story_vote(request, pk, direction)
    return redirect('story_view', pk)


def story_edit_log(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    story = get_object_or_404(Story, pk=pk)
    data = dict(
        edit_log=story.edit_log.order_by('date').select_related('user'),
        page_title="История редактирования рассказа \"{}\"".format(story.title),
    )
    return render(request, 'story_edit_log.html', data)


@login_required
@csrf_protect
def add(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = Story.bl.create(authors=[(request.user, True)], **form.cleaned_data)
            return redirect('story_edit', story.id)
    else:
        form = StoryForm(initial={'finished': 0, 'freezed': 0, 'original': 1, 'rating': 4})

    data = {
        'page_title': 'Новый рассказ',
        'form': form,
        'story_add': True
    }
    return render(request, 'story_work.html', data)


@login_required
@csrf_protect
def edit(request, pk):
    story = get_object_or_404(Story.objects, pk=pk)
    if not story.editable_by(request.user):
        raise PermissionDenied

    data = {
        'story_edit': True,
        'chapters': story.chapter_set.order_by('order'),
        'saved': False,
        'story': story
    }

    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story.bl.update(editor=request.user, **form.cleaned_data)
            data['saved'] = True
    else:
        form = StoryForm(instance=story)

    data['form'] = form
    data['page_title'] = 'Редактирование «{}»'.format(story.title)
    return render(request, 'story_work.html', data)


@login_required
@csrf_protect
def delete(request, pk):
    story = get_object_or_404(Story.objects, pk=pk)
    if not story.deletable_by(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        story.bl.delete()
        return redirect('index')

    return render(request, 'story_confirm_delete.html', {'page_title': 'Подтверждение удаления рассказа', 'story': story})


def story_download(request, story_id, filename, extension):
    from django.core.files.storage import default_storage as storage
    from ..downloads import get_format

    debug = settings.DEBUG and 'debug' in request.META['QUERY_STRING']

    story = get_story(request, story_id)
    fmt = get_format(extension)
    if fmt is None:
        raise Http404

    url = fmt.url(story)
    if url != request.path:
        return redirect(url)
    filepath = 'stories/%s/%s.%s' % (story_id, filename, extension)

    if (
        not storage.exists(filepath) or
        storage.modified_time(filepath) < story.updated or
        debug
    ):

        data = fmt.render(
            story=story,
            filename=filename,
            extension=extension,
            debug=debug,
        )
        if not debug:
            if storage.exists(filepath):
                storage.delete(filepath)
            storage.save(filepath, ContentFile(data))

    if not debug:
        return redirect(storage.url(filepath))
    else:
        response = HttpResponse(data)
        response['Content-Type'] = fmt.debug_content_type
        return response
