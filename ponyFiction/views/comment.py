# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from ponyFiction.forms.comment import CommentForm
from ponyFiction.models import Story

@login_required
@csrf_protect
def comment_story(request, story_id=False):
    try:
        story = Story.objects.accessible(user=request.user).get(pk=story_id)
    except Story.DoesNotExist:
        story = get_object_or_404(Story, pk=story_id)
        if not story.editable_by(request.user):
            raise PermissionDenied
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