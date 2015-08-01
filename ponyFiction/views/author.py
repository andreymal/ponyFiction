# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from cacheops import invalidate_obj

from ponyFiction.forms.author import AuthorEditEmailForm, AuthorEditPasswordForm, AuthorEditProfileForm, AuthorEditPrefsForm
from ponyFiction.models import Author, Comment, Story, StoryView


@csrf_protect
def author_info(request, user_id, comments_page):
    data = {}

    if user_id is None:
        author = request.user
        comments_list = Comment.objects.prefetch_related('story', 'author').filter(story__authors=request.user.id).order_by('-date').cache()
        data['all_views'] = StoryView.objects.filter(story__authors=author).cache().count()
        data['page_title'] = 'Мой кабинет'
        stories = author.story_set.prefetch_for_list.all().cache()
        template = 'author_dashboard.html'
    else:
        author = get_object_or_404(Author, pk=user_id)
        comments_list = author.comment_set.filter(story__in=Story.objects.accessible(user=request.user)).order_by('-date').cache()
        data['page_title'] = u'Автор: %s' % author.username
        stories = author.story_set.accessible(user=request.user)
        template = 'author_overview.html'

    comments_count = comments_list.count()
    series = author.series_set.all().cache()
    comments_paged = Paginator(comments_list, settings.COMMENTS_COUNT['author_page'], orphans=settings.COMMENTS_ORPHANS)
    num_pages = comments_paged.num_pages
    page_current = int(comments_page) if (0 < int(comments_page) <= num_pages) else 1
    comments = comments_paged.page(page_current)

    data.update({
        'author' : author,
        'stories': stories,
        'series' : series,
        'comments' : comments,
        'page_current': page_current,
        'num_pages': num_pages,
        'comments_count': comments_count
    })

    return render(request, template, data)


@login_required
@csrf_protect
def author_edit(request):
    author = request.user
    data = {}
    data['page_title'] = 'Настройки профиля'

    profile_form = None
    email_form = None
    password_form = None
    prefs_form = None

    if request.POST:
        invalidate_obj(author)
        if 'save_password' in request.POST:
            password_form = AuthorEditPasswordForm(request.POST, author=author, prefix='password_form')
            if password_form.is_valid():
                password_form.save()
                data['password_ok'] = True
                return redirect('auth_login')
            else:
                data['password_form_nfe'] = password_form.non_field_errors()
        if 'save_profile' in request.POST:
            profile_form = AuthorEditProfileForm(request.POST, instance=author, prefix='profile_form')
            if profile_form.is_valid():
                profile_form.save()
                data['profile_ok'] = True
        if 'save_email' in request.POST:
            email_form = AuthorEditEmailForm(request.POST, author=author, prefix='email_form')
            if email_form.is_valid():
                email_form.save()
                data['email_ok'] = True
        if 'save_prefs' in request.POST:
            prefs_form = AuthorEditPrefsForm(request.POST, author=author, prefix='prefs_form')
            if prefs_form.is_valid():
                prefs_form.save()
                data['prefs_ok'] = True

    if not profile_form:
        profile_form = AuthorEditProfileForm(instance=author, prefix='profile_form')
    if not email_form:
        email_form = AuthorEditEmailForm(author=author, prefix='email_form')
    if not password_form:
        password_form = AuthorEditPasswordForm(author=author, prefix='password_form')
    if not prefs_form:
        prefs_form = AuthorEditPrefsForm(author=author, prefix='prefs_form')
    data.update({'profile_form': profile_form, 'email_form': email_form, 'password_form': password_form, 'prefs_form': prefs_form})
    return render(request, 'author_profile_edit.html', data)

@login_required
@csrf_protect
@require_POST
def author_approve(request, user_id):
    raise PermissionDenied  # TODO: wtf is that?
    if request.user.is_staff:
        author = get_object_or_404(Author, pk=user_id)
        if author.approved:
            author.approved = False
        else:
            author.approved = True
        author.save(update_fields=['approved'])
        return redirect('author_overview', user_id)
    else:
        raise PermissionDenied


@login_required
@csrf_protect
@require_POST
def author_ban(request, user_id):
    if request.user.is_staff:
        author = get_object_or_404(Author, pk=user_id)
        if author.id != request.user.id:
            author.is_active = not author.is_active
            author.save(update_fields=['is_active'])
        return redirect('author_overview', user_id)
    else:
        raise PermissionDenied
