#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request

from django.http import Http404
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import login, get_backends
from django.shortcuts import render, redirect
from django.apps import apps
from django.views.decorators.csrf import csrf_protect

from .models import Migration
from .forms import MigrationNewForm, MigrationPasswordForm

User = apps.get_model(settings.AUTH_USER_MODEL)


@csrf_protect
def new(request):
    if request.method != 'POST':
        return render(request, 'migration_new.html', {'form': MigrationNewForm})

    postform = MigrationNewForm(request.POST)
    if not postform.is_valid():
        return render(request, 'migration_new.html', {'form': postform})

    user = User.objects.filter(username=postform.cleaned_data['author']).get()
    Migration.objects.filter(user=user).delete()
    migration = Migration(user=user)
    migration.save()

    return redirect('migration_approve', migration.auth_token)


def approve(request, auth_token):
    try:
        migration = Migration.objects.filter(auth_token=auth_token).get()
    except Migration.DoesNotExist:
        raise Http404

    approved = migration.approved

    if not approved:
        data = cache.get('stories_migration_%d' % migration.user.id)
        if not data:
            link = 'http://stories.everypony.ru/accounts/%d/' % migration.user.id
            req = urllib.request.Request(link)
            req.add_header('Accept', 'text/html, text/*, */*')
            req.add_header('Accept-Language', 'ru-RU,ru;q=0.8')
            req.add_header('User-Agent', 'Mozilla/5.0; stories.andreymal.org/0.1')
            try:
                data = urllib.request.urlopen(req).read().decode('utf-8', 'replace')
            except IOError as exc:
                return render(request, 'migration_approve.html', {'migration': migration, 'nodownload': str(exc), 'nodownload_link': link})
            # простейший анти-DDoS
            cache.set('stories_migration_%d' % migration.user.id, data, 2)
        approved = migration.inline_token in data

    if approved:
        if not migration.approved:
            migration.approved = True
            migration.save()
        return password(request, migration)

    return render(request, 'migration_approve.html', {'migration': migration})


@csrf_protect
def password(request, migration):
    if not migration.approved:
        return redirect('migration_approve', migration.auth_token)

    if request.method != 'POST':
        return render(request, 'migration_password.html', {'form': MigrationPasswordForm})

    postform = MigrationPasswordForm(request.POST)
    if not postform.is_valid():
        return render(request, 'migration_password.html', {'form': postform})

    user = migration.user
    user.set_password(postform.cleaned_data['password1'])
    user.save()
    backend = get_backends()[0]  # Hack to bypass `authenticate()`.
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    request.session.modified = True
    migration.delete()
    return redirect('index')
