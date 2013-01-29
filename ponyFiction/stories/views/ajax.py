# -*- coding: utf-8 -*-
from simplejson import loads, dumps
from django.conf import settings
from django.http import Http404, HttpResponse
from django.template import defaultfilters as filters
from django.shortcuts import redirect
from ponyFiction.stories.models import Story, Author, Comment, Chapter, Vote, Favorites
from ponyFiction.stories.utils.misc import dthandler, unicode_to_int_list

# TODO: Доделать исключения
# Перевести часть формирования данных с AJAX на обработку шаблонными фильтрами тут 
def ajax_comments(request, *args, **kwargs):
    type_request = kwargs.pop('type', None)   
    if request.method == 'GET' and request.is_ajax() and type_request is not None:
        try:
            data = loads(request.GET['data'])
        except:
            raise ValueError
        else:
            if type_request == 'story':
                comments_list = Story.objects.get(pk=kwargs.pop('story_id', 1)).comment_set.all()
            elif type_request == 'user':
                comments_list = Author.objects.get(pk=kwargs.pop('user_id', 1)).comment_set.all()
            elif type_request == 'new':
                comments_list = Comment.objects.order_by('-date').all()
    else:
        raise Http404
    message = makeCommentsAjaxResponse(comments_list, data)
    return HttpResponse(message)

def ajax_stories(request):
    if request.method == 'GET' and request.is_ajax():
        try:
            data = loads(request.GET['data'])
        except:
            raise ValueError
        else:
            stories_list = Story.objects.order_by('-date').all()
    else:
        raise Http404
    message = makeStoriesAjaxResponse(stories_list, data)
    return HttpResponse(message)

def ajax_favorites(request, user_id):
    if request.method == 'GET' and request.is_ajax():
        try:
            data = loads(request.GET['data'])
        except:
            raise ValueError
        else:
            if not Author.objects.filter(id=1).exists():
                raise Http404
            else:
                author = Author.objects.get(id=user_id)
                stories_list = author.favorites_story_set.order_by('-favorites_set__date')
    else:
        raise Http404
    message = makeStoriesAjaxResponse(stories_list, data)
    return HttpResponse(message)


def ajax_chapters(request):
    if request.method == 'GET' and request.is_ajax():
        try:
            data = loads(request.GET['data'])
        except:
            raise ValueError
        else:
            chapters_list = Chapter.objects.order_by('-date').all()
    else:
        raise Http404
    message = makeChaptersAjaxResponse(chapters_list, data)
    return HttpResponse(message)

#data = {'type' : 'paged', 'pointer' : 'next', 'page_current' : 3}
#data = {'type' : 'direct', 'page_id' : 26}
#data = {'type' : 'flow', 'scroll_id' : 4}

def makeCommentsAjaxResponse(comments_list, data):
    if data['type'] == 'paged' or data['type'] == 'direct':
        comments_page = processPageComments(comments_list, data)
    elif data['type'] == 'flow':
        comments_page = processFlow(comments_list, data, objects_type='comments')
    new_list = []
    for cmt in comments_page:
        new_list.append({'comment_id': cmt.pk,
                         'author_id': cmt.author.id,
                         'story_id': cmt.in_story_id,
                         'story_title': cmt.in_story.title,
                         'author_name': cmt.author.username,
                         'date': cmt.date,
                         'text': cmt.text})
    return dumps(new_list, default=dthandler)
def processPageComments(comments_list, data):
    from django.core.paginator import Paginator
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['load'], orphans=settings.COMMENTS_ORPHANS)
    
    if data['type'] == 'paged' and data.has_key('pointer') and data.has_key('page_current'):
        pointer = data['pointer']
        page_current = data['page_current']
        if paged.num_pages == 1:
            pointer = 'first'
        if pointer == 'first':
            comments_page = paged.page(1)
        elif pointer == 'prev':
            page_num = int(page_current)
            page_num -= 1
            if page_num > 0:
                comments_page = paged.page(page_num)
            else:
                comments_page = paged.page(1)
        elif pointer == 'next':
            page_num = int(page_current)
            if page_num < paged.num_pages:
                page_num += 1
                comments_page = paged.page(page_num)
            else:
                comments_page = paged.page(paged.num_pages)
        elif pointer == 'last':
            page_num = int(page_current)
            comments_page = paged.page(paged.num_pages)
    elif data['type'] == 'direct' and data.has_key('page_id'):
        try:
            d_i = int(data['page_id'])
        except ValueError:
            comments_page = paged.page(1)
        else:
            if ((d_i <= paged.num_pages) and (d_i >= 1)):
                comments_page = paged.page(d_i)
            else:
                comments_page = paged.page(1)
    else:
        comments_page = paged.page(1)
    return comments_page.object_list

#data = {'type' : 'flow', 'scroll_id' : 4}
def makeStoriesAjaxResponse(stories_list, data):
    stories_page = processFlow(stories_list, data, objects_type='stories')
    new_list = []
    for story in stories_page:
        story_authors_all = story.authors.all()
        story_categories_all = story.categories.all()
        story_characters_all = story.characters.all()
        story_authors=[]
        story_categories=[]
        story_characters=[]
        for author in story_authors_all:
            story_authors.append({'author_id': author.id, 'author_name': author.username})
        for category in story_categories_all:
            story_categories.append({'category_id': category.id, 'category_name': category.name})
        for character in story_characters_all:
            story_characters.append({'character_id': character.id, 'character_name': character.name})
        story_list_item = {
                           'story_id': story.id,
                           'story_title': story.title,
                           'story_summary': story.summary,
                           'story_authors': story_authors,
                           'story_categories': story_categories,
                           'story_characters': story_characters,
                           'story_vote_up_count': story.vote_up_count(),
                           'story_vote_down_count': story.vote_down_count(),
                           'story_words': story.words
                           }
        new_list.append(story_list_item)  
    return dumps(new_list, default=dthandler)

def makeChaptersAjaxResponse(chapters_list, data):
    chapters_page = processFlow(chapters_list, data, objects_type='chapters')
    new_list = []
    for chapter in chapters_page:
        chapter_list_item={
                           'chapter_id': chapter.id,
                           'chapter_title': chapter.title,
                           'chapter_order': chapter.order,
                           'story_id': chapter.in_story.id,
                           'story_title': chapter.in_story.title,
                           'author_id': chapter.in_story.authors.all()[0].id,
                           'author_name': chapter.in_story.authors.all()[0].username,
                           'date': filters.date(chapter.date, "d.m.Y"),
                           'text_snippet': filters.truncatewords_html(chapter.text, 50)
                           }
        new_list.append(chapter_list_item)
    return dumps(new_list, default=dthandler)  
def processFlow(object_list, data, objects_type):
    if data.has_key('scroll_id'):
        try:
            s_i = int(data['scroll_id'])
        except ValueError:
            scroll_id = 1
        else:
            scroll_id = s_i if (s_i > 0) else 1
        if objects_type == 'comments':
            o_l = object_list[settings.COMMENTS_COUNT['stream']*(scroll_id-1):settings.COMMENTS_COUNT['stream']*scroll_id]
        elif objects_type == 'stories':
            o_l = object_list[settings.STORIES_COUNT['stream']*(scroll_id-1):settings.STORIES_COUNT['stream']*scroll_id]
        elif objects_type == 'chapters':
            o_l = object_list[settings.CHAPTERS_COUNT['stream']*(scroll_id-1):settings.CHAPTERS_COUNT['stream']*scroll_id]
        return o_l

# TODO: Всерьёз оптимизировать! Эта функция слишком, СЛИШКОМ медленно отрабатывает!

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
            # Достаем голос
            vote = story.vote.get(author=request.user)
        except Vote.DoesNotExist:
            # Если автор не голосовал ещё
            vote = Vote.objects.create()
            vote.author = request.user
            vote.ip = request.META['REMOTE_ADDR']
            vote.direction = direction
            vote.save()
            story.vote.add(vote)
        else:
            # Иначе просто обновляем голос автора
            vote.direction = direction
            vote.save()
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