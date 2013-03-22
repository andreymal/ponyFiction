# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from ponyFiction.forms.author import AuthorEditEmailForm, AuthorEditPasswordForm, AuthorEditProfileForm 
from ponyFiction.models import Author, Story, Comment, Vote, StoryView
from ponyFiction.views.object_lists import ObjectList

@login_required
@csrf_protect
def author_info(request, user_id=None):
    data = {}
    if user_id is None:
        author = request.user
        comments_list = Comment.objects.filter(story__authors=request.user.id)
        data['all_views'] = StoryView.objects.filter(story__authors=author).count()
        data['page_title'] = 'Мой кабинет'
        data['stories'] = author.story_set.all()
        template = 'author_dashboard.html'
    else:
        author = get_object_or_404(Author, pk=user_id)
        comments_list = author.comment_set.all()
        data['page_title'] = u'Автор: %s' % author.username
        data['stories'] = author.story_set.filter(draft=False, approved=True)
        template = 'author_overview.html'
    comments_count = comments_list.count()
    published_stories = Story.published.filter(authors=author).count()
    series = author.series_set.all()
    votes = [Vote.objects.filter(plus=True).filter(story__authors__id=author.id).count(),
             Vote.objects.filter(minus=True).filter(story__authors__id=author.id).count()]
    comments_paged = Paginator(comments_list, settings.COMMENTS_COUNT['author_page'], orphans=settings.COMMENTS_ORPHANS)
    comments = comments_paged.page(1)
    num_pages = comments_paged.num_pages
    data.update({
            'author' : author,
            'published_stories': published_stories,
            'series' : series,
            'comments' : comments,
            'num_pages': num_pages,
            'comments_count': comments_count,
            'votes': votes
            })
    return render(request, template, data)


@login_required
@csrf_protect
def author_edit(request):
    author = request.user
    data = {}
    data['page_title'] = 'Настройки профиля'
    if request.POST:
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
        if 'save_password' in request.POST:
            password_form = AuthorEditPasswordForm(request.POST, author=author, prefix='password_form')
            if password_form.is_valid():
                password_form.save()
                data['password_ok'] = True
            else:
                data['password_form_nfe'] = password_form.non_field_errors()
    profile_form = AuthorEditProfileForm(instance=author, prefix='profile_form')
    email_form = AuthorEditEmailForm(author=author, prefix='email_form')
    password_form = AuthorEditPasswordForm(author=author, prefix='password_form')
    data.update({'profile_form': profile_form, 'email_form': email_form, 'password_form': password_form})
    return render(request, 'author_profile_edit.html', data)

class CommentsAuthor(ObjectList):
    
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