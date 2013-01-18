from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ponyFiction.stories.models import Story
from ponyFiction.forms import StoryAddComment
from django.contrib.auth.decorators import login_required

@login_required
@csrf_protect
def comment_story(request, **kwargs):
    story_id = kwargs.pop('story_id', None)
    story = Story.objects.get(pk=story_id)
    author = request.user 
    comment_form = StoryAddComment(request.POST)
    ip = request.META['REMOTE_ADDR']
    
    new_comment = comment_form.save(commit=False)
    new_comment.author = author
    new_comment.in_story = story
    new_comment.ip = ip
    new_comment.save()
        
    return HttpResponseRedirect(reverse('story_view', args=(story_id, )))