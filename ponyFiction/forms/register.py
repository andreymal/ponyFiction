#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from captcha.fields import ReCaptchaField
from ponyFiction.apis.captcha.fields import ReCaptchaField
from registration.forms import RegistrationFormUniqueEmail
from django.forms import CharField, EmailField, PasswordInput, RegexField, TextInput


attrs_dict = {'class': 'required form-control'}
username_field = RegexField(
    regex=r'^[0-9a-zA-Z\u0430-\u044f\u0410-\u042f\u0451\u0401_@+-.. ]+$',
    widget=TextInput(attrs=dict(attrs_dict, maxlength=32)),
    max_length=32,
    label='Логин',
    help_text='Только русские/латинские буквы, цифры, пробел, точка и символы _ @ + -',
    error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине - он может содержать только русские/латинские буквы, цифры, пробел, точку и символы _ @ + -'}
)


class AuthorRegistrationForm(RegistrationFormUniqueEmail):
    username = username_field
    email = EmailField(
        widget=TextInput(attrs=dict(attrs_dict, maxlength=75)),
        max_length=75,
        label='Электропочта',
        help_text='Адрес электронной почты для активации аккаунта',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в адресе e-mail: похоже, он неправильный'}
    )
    password1 = CharField(
        widget=PasswordInput(attrs=attrs_dict, render_value=False),
        label="Пароль",
        help_text='Выбирайте сложный пароль',
        )
    password2 = CharField(
        widget=PasswordInput(attrs=attrs_dict, render_value=False),
        label="Пароль (опять)",
        help_text='Повторите пароль, чтобы не забыть',
        )
    recaptcha = ReCaptchaField(
        label="Капча",
        error_messages={'captcha_invalid': 'Это какая-то неправильная капча. Пожалуйста, введите снова.'}
        )
