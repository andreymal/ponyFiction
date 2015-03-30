# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from ponyFiction.models import Author, Character, CharacterGroup, Category, Classifier, Rating, Series, Story, Chapter, Comment, BetaReading


class StoryAdmin(admin.ModelAdmin):
    exclude = ('vote',)

class ChapterAdmin(admin.ModelAdmin):
    raw_id_fields = ('story',)
    
admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register([Character, CharacterGroup, Category, Classifier, Rating, Series, Comment, BetaReading])



class AuthorChangeForm(UserChangeForm):
    username =forms.RegexField(
        regex=ur'^[0-9a-zA-Z\u0430-\u044f\u0410-\u042f\u0451\u0401_@+-.. ]+$',
        widget=forms.TextInput(attrs=dict(maxlength=32)),
        max_length=32,
        label='Логин',
        help_text='Только русские/латинские буквы, цифры, пробел, точка и символы _ @ + -',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине - он может содержать только русские/латинские буквы, цифры, пробел, точку и символы _ @ + -'}
    )

    class Meta:
        model = Author

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