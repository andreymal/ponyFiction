# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from json import dumps
from ponyFiction.models import Author, Story, Comment, Chapter, Favorites, Bookmark
from ponyFiction.utils.misc import unicode_to_int_list
from ponyFiction.views.object_lists import ObjectList

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
    
    def get_queryset(self):
        story = get_object_or_404(Story, pk=self.kwargs['story_id'])
        return story.comment_set.all()
    
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
    
    def get_queryset(self):
        if self.kwargs['user_id'] is None:
            return Comment.objects.filter(story__authors=self.request.user.id)
        else:
            author = get_object_or_404(Author, pk=self.kwargs['user_id'])
            return author.comment_set.all()

class ConfirmDeleteStory(TemplateView):
    """ Отрисовка модального окна подтверждения удаления рассказа """
    
    template_name = 'includes/story_delete_confirm.html'
    
    def get_context_data(self, **kwargs):
        story = get_object_or_404(Story, pk=self.kwargs['story_id'])
        return {'story_id': story.id, 'story_title': story.title}
 
@login_required
@csrf_protect
def story_delete_ajax(request, story_id):
    """ Удаление рассказа по AJAX """
    
    if request.is_ajax() and request.method == 'POST':
        story = get_object_or_404(Story, pk=story_id)
        if story.is_editable_by(request.user):
            story.delete()
            return HttpResponse(story_id)
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_publish_ajax(request, story_id):
    """ Публикация рассказа по AJAX """
    
    if request.is_ajax() and request.method == 'POST':
        story = get_object_or_404(Story, pk=story_id)
        if story.is_editable_by(request.user):
            if story.draft:
                story.draft = False
            else:
                story.draft = True
            story.save(update_fields=['draft'])
            return HttpResponse(story_id)
    else:
        raise PermissionDenied
    
@login_required
@csrf_protect
def story_approve_ajax(request, story_id):
    """ Одобрение рассказа по AJAX """

    if request.user.is_staff and request.is_ajax() and request.method == 'POST':
        story = get_object_or_404(Story, pk=story_id)
        if story.approved:
            story.approved = False
        else:
            story.approved = True
        story.save(update_fields=['approved'])
        return HttpResponse(story_id)
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_bookmark_ajax(request, story_id):
    """ Добавление рассказа в закладки """
    
    if request.is_ajax() and request.method == 'POST':
        story = get_object_or_404(Story.objects.published, pk=story_id)
        (bookmark, created) = Bookmark.objects.get_or_create(story=story, author=request.user)
        if not created:
            bookmark.delete()
        return HttpResponse(story_id)
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_favorite_ajax(request, story_id):
    """ Добавление рассказа в избранное """
    if request.is_ajax() and request.method == 'POST':
        story = get_object_or_404(Story.objects.published, pk=story_id)
        (favorite, created) = Favorites.objects.get_or_create(story=story, author=request.user)
        if not created:
            favorite.delete()
        return HttpResponse(story_id)
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_vote_ajax(request, story_id, direction):
    if request.is_ajax() and request.method == 'POST':
        story = get_object_or_404(Story.objects.published, pk=story_id)
        direction = True if (direction == 'plus') else False
        if story.is_editable_by(request.user):
            return HttpResponse(dumps([story.vote_up_count(), story.vote_down_count()]))
        vote = story.vote.get_or_create(author=request.user)[0]
        if direction:
            vote.plus = True
            vote.minus = None
        else:
            vote.plus = None
            vote.minus = True
        vote.save(update_fields=['plus', 'minus'])
        story.vote.add(vote)
        return HttpResponse(dumps([story.vote_up_count(), story.vote_down_count()]))
    else:
        raise PermissionDenied
    
@login_required
@csrf_protect
def chapter_sort(request, story_id):
    """ Сортировка глав """
    story = get_object_or_404(Story.objects.accessible, pk=story_id)
    if story.is_editable_by(request.user) and request.is_ajax() and request.method == 'POST':
        new_order = unicode_to_int_list(request.POST.getlist('chapters[]'))
        if (not new_order or story.chapter_set.count() != len(new_order)):
                return HttpResponse('Bad request. Incorrect list!', status=400)
        else:
            for new_order_id, chapter_id in enumerate(new_order):
                chapter = Chapter.objects.get(pk=chapter_id)
                chapter.order = new_order_id+1
                chapter.save(update_fields=['order'])
            return HttpResponse('Done')
    else:
        raise PermissionDenied

