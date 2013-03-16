from django.views.decorators.csrf import csrf_protect
from ponyFiction.models import Story
from ponyFiction.forms.comment import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
@csrf_protect
def comment_story(request, story_id=False):
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return redirect('index')
    else:
        author = request.user 
        comment_form = CommentForm(request.POST)
        ip = request.META['REMOTE_ADDR']
        new_comment = comment_form.save(commit=False)
        new_comment.author = author
        new_comment.story = story
        new_comment.ip = ip
        new_comment.save()
        return redirect('story_view', story_id)