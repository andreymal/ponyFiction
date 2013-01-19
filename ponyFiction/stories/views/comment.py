from django.views.decorators.csrf import csrf_protect
from ponyFiction.stories.models import Story
from ponyFiction.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
@csrf_protect
def comment_story(request, story_id=False):
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return redirect('story_view', kwargs={'story_id': story_id})
    else:
        author = request.user 
        comment_form = CommentForm(request.POST)
        ip = request.META['REMOTE_ADDR']
        new_comment = comment_form.save(commit=False)
        new_comment.author = author
        new_comment.in_story = story
        new_comment.ip = ip
        new_comment.save()
        return redirect('story_view', kwargs={'story_id': story_id})