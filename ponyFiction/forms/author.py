# -*- coding: utf-8 -*-
from ponyFiction.models import Author, Category
from django.forms import CharField, EmailField, Form, ModelForm, PasswordInput, RegexField, TextInput, Textarea, ValidationError, URLField
from ponyFiction.utils.misc import obj_to_int_list
from ponyFiction.widgets import StoriesButtons, StoriesRadioButtons
from django.forms.models import ModelMultipleChoiceField
from django.forms.fields import ChoiceField


class AuthorEditProfileForm(ModelForm):
    attrs_dict = {'class': 'form-control'}
    bio = CharField(
        widget=Textarea(attrs=dict(attrs_dict, maxlength=2048, placeholder='Небольшое описание, отображается в профиле')),
        max_length=2048,
        label='Пару слов о себе',
        required=False,
    )
    jabber = EmailField(
        widget=TextInput(attrs=dict(attrs_dict, maxlength=75, placeholder='Адрес jabber-аккаунта')),
        max_length=75,
        label='Jabber ID (XMPP)',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в адресе jabber: похоже, он неправильный'},
        required=False,
        help_text='Пример: user@server.com',
    )
    skype = RegexField(
        regex=r'^[a-zA-Z0-9\._-]+$',
        widget=TextInput(attrs=dict(attrs_dict, maxlength=32, placeholder='Логин skype')),
        max_length=32,
        label='Skype ID',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине skype: похоже, он неправильный'},
        required=False
    )
    tabun = RegexField(
        regex=r'^[a-zA-Z0-9-_]+$',
        widget=TextInput(attrs=dict(attrs_dict, maxlength=32)),
        max_length=32,
        label='Логин на Табуне',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в имени пользователя: похоже, оно неправильно'},
        required=False
    )
    forum = URLField(
        widget=TextInput(attrs=dict(attrs_dict, maxlength=32, placeholder='URL вашего профиля')),
        max_length=72,
        label='Профиль на Форуме',
        help_text='Вставьте полную ссылку на профиль',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку адресе профиля: похоже, он неправильный.'},
        required=False
    )
    vk = RegexField(
        regex=r'^[a-zA-Z0-9\._-]+$',
        widget=TextInput(attrs=dict(attrs_dict, maxlength=32)),
        max_length=32,
        label='Логин ВКонтакте',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине ВК: похоже, он неправильный'},
        required=False
    )

    class Meta:
        model = Author
        fields = ('bio', 'jabber', 'skype', 'tabun', 'forum', 'vk')


class AuthorEditPrefsForm(Form):
    checkbox_attrs = {
        'btn_attrs': {'type': 'button', 'class': 'btn btn-default'},
        'data_attrs': {'class': 'hidden'},
        'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-checkbox', 'role': 'group'},
        'data_container_attrs': {'class': 'buttons-data'},
    }
    radio_attrs = {
        'btn_attrs': {'type': 'button', 'class': 'btn btn-default'},
        'data_attrs': {'class': 'hidden'},
        'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-radio', 'role': 'group'},
        'data_container_attrs': {'class': 'buttons-data'},
    }
    excluded_categories = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    detail_view = ChoiceField(
        choices=[(0, 'Кратко'), (1, 'Подробно')],
        required=True,
        widget=StoriesRadioButtons(attrs=radio_attrs),
    )
    nsfw = ChoiceField(
        choices=[(0, 'Показать'), (1, 'Скрыть')],
        required=True,
        widget=StoriesRadioButtons(attrs=radio_attrs),
    )

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(AuthorEditPrefsForm, self).__init__(*args, **kwargs)
        if self.author:
            self.fields['excluded_categories'].initial = ','.join(str(x) for x in self.author.excluded_categories)
            self.fields['detail_view'].initial = self.author.detail_view
            self.fields['nsfw'].initial = self.author.nsfw

    def save(self):
        author = self.author
        excluded_categories = self.cleaned_data['excluded_categories']
        author.excluded_categories = obj_to_int_list(excluded_categories)
        author.detail_view = bool(int(self.cleaned_data['detail_view']))
        author.nsfw = bool(int(self.cleaned_data['nsfw']))
        author.save(update_fields=['excluded_categories', 'detail_view', 'nsfw'])


class AuthorEditEmailForm(Form):
    attrs_dict = {'class': 'form-control'}

    email = EmailField(
        widget=TextInput(attrs=dict(attrs_dict, maxlength=75, placeholder='Адрес электронной почты')),
        max_length=75,
        label='Электропочта',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в адресе e-mail: похоже, он неправильный'}
    )
    password = CharField(
        widget=PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Пароль",
        help_text='Для безопасной смены почты введите пароль',
    )

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(AuthorEditEmailForm, self).__init__(*args, **kwargs)
        if self.author:
            self.fields['email'].initial = self.author.email

    def clean(self):
        cleaned_data = super(AuthorEditEmailForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            if not self.author.check_password(password):
                raise ValidationError('Неверный пароль')
        return cleaned_data

    def save(self):
        author = self.author
        email = self.cleaned_data['email']
        author.email = email
        author.save(update_fields=['email'])


class AuthorEditPasswordForm(Form):
    attrs_dict = {'class': 'form-control'}

    old_password = CharField(
        widget=PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Старый пароль",
        help_text='Для безопасной смены пароля введите старый пароль',
        error_messages={'required': 'Поле нельзя оставить пустым'}
    )
    new_password_1 = CharField(
        widget=PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Новый пароль",
        help_text='Выбирайте сложный пароль',
        error_messages={'required': 'Поле нельзя оставить пустым'}
    )
    new_password_2 = CharField(
        widget=PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Новый пароль (опять)",
        help_text='Повторите новый пароль, чтобы не забыть',
        error_messages={'required': 'Поле нельзя оставить пустым'}
        )

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(AuthorEditPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AuthorEditPasswordForm, self).clean()
        old_password = cleaned_data.get('old_password')
        new_password_1 = cleaned_data.get('new_password_1')
        new_password_2 = cleaned_data.get('new_password_2')
        nfe = []
        if not(old_password and new_password_1 and new_password_2):
            nfe.append('Введены не все данные')
        else:
            if not self.author.check_password(old_password):
                nfe.append('Старый пароль неверный')
            if new_password_1 != new_password_2:
                nfe.append('Пароли не совпадают')
        if nfe:
            raise ValidationError(nfe)
        return cleaned_data

    def save(self):
        author = self.author
        password = self.cleaned_data['new_password_1']
        author.set_password(password)
        author.save()
