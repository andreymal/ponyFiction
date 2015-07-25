#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import CharField, Field, Form, TextInput, PasswordInput
from django.conf import settings
from django.apps import apps
from django.core.exceptions import ValidationError

User = apps.get_model(settings.AUTH_USER_MODEL)

class MigrationNewForm(Form):
    author = CharField(required=True, label='Ник на {}'.format(settings.MIGRATION_NAME), max_length=255, widget=TextInput(attrs=dict(maxlength=255)),)

    def clean_author(self):
        try:
            author = User.objects.filter(username=self.cleaned_data['author']).get()
        except:
            raise ValidationError('Нет такого пользователя')
        return self.cleaned_data['author']


class MigrationPasswordForm(Form):
    password1 = CharField(
        widget=PasswordInput(render_value=False),
        label="Пароль",
        help_text='Выбирайте сложный пароль',
    )
    password2 = CharField(
        widget=PasswordInput(render_value=False),
        label="Пароль (опять)",
        help_text='Повторите пароль, чтобы не забыть',
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password_1 = cleaned_data.get('password1')
        new_password_2 = cleaned_data.get('password2')
        nfe = []
        if not(new_password_1 and new_password_2):
            nfe.append('Введены не все данные')
        else:
            if new_password_1 != new_password_2:
                nfe.append('Пароли не совпадают')
        if nfe:
            raise ValidationError(nfe)
        return cleaned_data
