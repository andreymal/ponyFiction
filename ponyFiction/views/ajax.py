# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from json import dumps
from ponyFiction.models import Story, Chapter, Vote, Favorites
from ponyFiction.utils.misc import unicode_to_int_list
from ponyFiction.views.object_lists import ObjectList
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied

class CommentsStory(ObjectList):
    ''' Подгрузка комментариев к рассказу'''
    
    context_object_name = 'comments'
    paginate_by = settings.COMMENTS_COUNT['author_page']

    @property
    def template_name(self):
        return 'includes/comments.html'
    
    @property
    def page_title(self):
        return None
    
    def get_queryset(self):
        story = get_object_or_404(Story, pk=self.kwargs['story_id'])
        return story.comment_set.all()
    
class ConfirmDeleteStory(TemplateView):
    ''' Отрисовка модального окна подтверждения удаления рассказа '''
    
    template_name = 'includes/story_delete_confirm.html'
    
    def get_context_data(self, **kwargs):
        story = get_object_or_404(Story, pk=self.kwargs['story_id'])
        return {'story_id': story.id, 'story_title': story.title}
    
@login_required
@csrf_protect
def story_delete_ajax(request, story_id):
    ''' Удаление рассказа по AJAX '''
    
    story = get_object_or_404(Story, pk=story_id)
    if story.is_editable_by(request.user) and request.is_ajax() and request.method == 'POST':
        story.delete()
        return HttpResponse(story_id)
    else:
        raise PermissionDenied

@login_required
@csrf_protect
def story_publish_ajax(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if story.is_editable_by(request.user) and request.is_ajax() and request.method == 'POST':
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
    ''' Одобрение рассказа по AJAX '''
    
    story = get_object_or_404(Story, pk=story_id)
    if story.is_editable_by(request.user) and request.is_ajax() and request.method == 'POST' and request.user.is_staff:
        if story.approved:
            story.approved = False
        else:
            story.approved = True
        story.save(update_fields=['approved'])
        return HttpResponse(story_id)
    else:
        raise PermissionDenied
    

def sort_chapters(request, story_id):
    try:
        story = Story.objects.get(pk=story_id)    
        assert request.POST
        assert request.is_ajax()
    except Story.DoesNotExist:
        return HttpResponse("Story doesn't exist!", status=404)
    except AssertionError:
        return redirect('index')
    else:
        if not request.user.is_authenticated():
            return HttpResponse('Unauthorized user!', status=401)
        elif not (story.authors.filter(id=request.user.id)):
            return HttpResponse('Forbidden. You are not author!', status=403)
        else:
            new_order = unicode_to_int_list(request.POST.getlist('chapters[]'))   
            if (not new_order or story.chapter_set.count() != len(new_order)):
                return HttpResponse('Bad request. Incorrect list!', status=400)
            else:
                for new_order_id, chapter_id in enumerate(new_order):
                    chapter = Chapter.objects.get(pk=chapter_id)
                    chapter.order = new_order_id+1
                    chapter.save(update_fields=['order'])
                return HttpResponse('Done', status=200)

def story_vote(request, story_id):
    try:
        story = Story.objects.get(pk=story_id)    
        assert request.POST
        assert request.is_ajax()
    except Story.DoesNotExist:
        return HttpResponse("Story doesn't exist!", status=404)
    except AssertionError:
        return redirect('index')
    else:
        if not request.user.is_authenticated():
            return HttpResponse('Unauthorized user!', status=401)
        direction = True if (request.POST.get('vote', True) == '1') else False
        if (story.authors.filter(id=request.user.id)):
            return HttpResponse(dumps([story.vote_up_count(), story.vote_down_count()]), status=200)
        try:
            vote = story.vote.get(author=request.user)
        except Vote.DoesNotExist:
            if direction:
                story.vote.add(Vote.objects.create(author=request.user, ip=request.META['REMOTE_ADDR'], plus=True))
            else:
                story.vote.add(Vote.objects.create(author=request.user, ip=request.META['REMOTE_ADDR'], minus=True))
        else:
            if direction:
                vote.plus = True
                vote.minus = None
            else:
                vote.plus = None
                vote.minus = True
            vote.save(update_fields=['plus', 'minus'])
        return HttpResponse(dumps([story.vote_up_count(), story.vote_down_count()]), status=200)
    
def favorites_work(request, story_id, chapter_id=None):
    try:
        story = Story.objects.get(pk=story_id)    
        assert request.method == 'POST'
        assert request.is_ajax()
    except Story.DoesNotExist:
        return HttpResponse("Story doesn't exist!", status=404)
    except AssertionError:
        return redirect('index')
    else:
        if not request.user.is_authenticated():
            return HttpResponse('Unauthorized user!', status=401)            
        if Favorites.objects.filter(author=request.user, story=story).exists():
            Favorites.objects.get(author=request.user, story=story).delete()
            return HttpResponse('0', status=200)
        else:
            Favorites.objects.create(author=request.user, story=story)
            return HttpResponse('1', status=200)