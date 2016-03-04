#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from ponyFiction.forms.register import username_field
from ponyFiction.models import (
    Author, Character, CharacterGroup, Category, Classifier,
    Rating, Series, Story, Chapter, Comment, BetaReading, StaticPage
)


class StoryAdmin(admin.ModelAdmin):
    exclude = ('vote',)


class ChapterAdmin(admin.ModelAdmin):
    raw_id_fields = ('story',)

admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register([Character, CharacterGroup, Category, Classifier])
admin.site.register([Rating, Series, Comment, BetaReading, StaticPage])


class AuthorChangeForm(UserChangeForm):
    username = username_field

    class Meta:
        model = Author
        fields = '__all__'


class AuthorAdmin(UserAdmin):
    form = AuthorChangeForm

    list_display = ('username', 'email', 'last_name', 'first_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': (
                'first_name', 'last_name', 'email', 'bio', 'jabber', 'skype', 'tabun', 'forum', 'vk'
            )}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Groups'), {'fields': ('groups',)}),
    )

admin.site.register(Author, AuthorAdmin)
