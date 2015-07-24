# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import ponyFiction.fields
import django.contrib.auth.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('bio', models.TextField(max_length=2048, verbose_name='О себе', blank=True)),
                ('jabber', models.EmailField(max_length=75, verbose_name='Jabber', blank=True)),
                ('skype', models.CharField(max_length=256, verbose_name='Skype ID', blank=True)),
                ('tabun', models.CharField(max_length=256, verbose_name='Табун', blank=True)),
                ('forum', models.URLField(verbose_name='Форум', blank=True)),
                ('vk', models.URLField(verbose_name='VK', blank=True)),
                ('excluded_categories', ponyFiction.fields.SeparatedValuesField(null=True, verbose_name='Скрытые категории', max_length=200)),
                ('detail_view', models.BooleanField(verbose_name='Детальное отображение рассказов', default=False)),
                ('nsfw', models.BooleanField(verbose_name='NSFW без предупреждения', default=False)),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', to='auth.Group', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission', related_name='user_set')),
            ],
            options={
                'verbose_name': 'автор',
                'verbose_name_plural': 'авторы',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата последнего просмотра автором', auto_now_add=True)),
                ('last_views', models.IntegerField(verbose_name='Последнее количество просмотров', default=0)),
                ('last_comments', models.IntegerField(verbose_name='Последнее количество комментариев', default=0)),
                ('last_vote_up', models.IntegerField(verbose_name="Последнее количество голосов 'За'", default=0)),
                ('last_vote_down', models.IntegerField(verbose_name="Последнее количество голосов 'Против'", default=0)),
                ('author', models.ForeignKey(null=True, verbose_name='Автор просмотра', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'активность',
                'verbose_name_plural': 'активность',
            },
        ),
        migrations.CreateModel(
            name='BetaReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('checked', models.BooleanField(verbose_name='Вычитано бетой', default=False)),
                ('beta', models.ForeignKey(null=True, verbose_name='Бета', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'вычитка',
                'verbose_name_plural': 'вычитки',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата добавления в список для прочтения', auto_now_add=True)),
                ('author', models.ForeignKey(null=True, verbose_name='Автор', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'закладка рассказа',
                'verbose_name_plural': 'закладки рассказов',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(max_length=4096, verbose_name='Описание', blank=True)),
                ('name', models.CharField(verbose_name='Название', max_length=256)),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'жанры',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)),
                ('mark', models.PositiveSmallIntegerField(verbose_name='Оценка', default=0)),
                ('notes', models.TextField(verbose_name='Заметки к главе', blank=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name='Порядок глав в рассказу', default=1)),
                ('title', models.CharField(verbose_name='Название', max_length=512)),
                ('text', models.TextField(verbose_name='Текст главы', blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('words', models.IntegerField(verbose_name='Количество слов в главе', default=0)),
            ],
            options={
                'verbose_name': 'глава',
                'verbose_name_plural': 'главы',
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(max_length=4096, verbose_name='Биография', blank=True)),
                ('name', models.CharField(verbose_name='Имя', max_length=256)),
            ],
            options={
                'verbose_name': 'персонаж',
                'verbose_name_plural': 'персонажи',
            },
        ),
        migrations.CreateModel(
            name='CharacterGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Название группы', max_length=256)),
                ('description', models.TextField(max_length=4096, verbose_name='Описание группы', blank=True)),
            ],
            options={
                'verbose_name': 'Группа персонажей',
                'verbose_name_plural': 'Группы персонажей',
            },
        ),
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(max_length=4096, verbose_name='Описание', blank=True)),
                ('name', models.CharField(verbose_name='Название', max_length=256)),
            ],
            options={
                'verbose_name': 'событие',
                'verbose_name_plural': 'события',
            },
        ),
        migrations.CreateModel(
            name='CoAuthorsSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('approved', models.BooleanField(verbose_name='Подтверждение', default=False)),
                ('author', models.ForeignKey(null=True, verbose_name='Автор', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoAuthorsStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('approved', models.BooleanField(verbose_name='Подтверждение', default=False)),
                ('author', models.ForeignKey(verbose_name='Автор', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('ip', models.GenericIPAddressField(verbose_name='IP комментатора', default='0.0.0.0')),
                ('author', models.ForeignKey(null=True, verbose_name='Автор комментария', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата добавления в избранное', auto_now_add=True)),
                ('author', models.ForeignKey(null=True, verbose_name='Автор', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранное',
            },
        ),
        migrations.CreateModel(
            name='InSeriesPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name='Порядок рассказов в серии', default=1)),
                ('request', models.BooleanField(verbose_name='Запрос на добавление', default=False)),
                ('answer', models.BooleanField(verbose_name='Ответ на запрос', default=False)),
            ],
            options={
                'verbose_name': 'добавление в серию',
                'verbose_name_plural': 'добавления в серию',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(max_length=4096, verbose_name='Описание', blank=True)),
                ('name', models.CharField(verbose_name='Название', max_length=256)),
            ],
            options={
                'verbose_name': 'рейтинг',
                'verbose_name_plural': 'рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cover', models.BooleanField(verbose_name='Наличие обложки', default=False)),
                ('date', models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)),
                ('draft', models.BooleanField(verbose_name='Черновик', default=True)),
                ('finished', models.BooleanField(verbose_name='Оконченность cерии', default=False)),
                ('freezed', models.BooleanField(verbose_name='Статус "заморозки"', default=False)),
                ('mark', models.PositiveSmallIntegerField(verbose_name='Оценка', default=0)),
                ('notes', models.TextField(max_length=8192, verbose_name='Заметки к серии', blank=True)),
                ('original', models.BooleanField(verbose_name='Статус оригинала', default=True)),
                ('summary', models.TextField(verbose_name='Общее описание', max_length=8192)),
                ('title', models.CharField(verbose_name='Название', max_length=512)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('views', models.IntegerField(verbose_name='Количество просмотров', default=0)),
                ('authors', models.ManyToManyField(verbose_name='Авторы', to=settings.AUTH_USER_MODEL, through='ponyFiction.CoAuthorsSeries')),
            ],
            options={
                'verbose_name': 'серия',
                'verbose_name_plural': 'серии',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Название', max_length=512)),
                ('cover', models.BooleanField(verbose_name='Наличие обложки', default=False, editable=False)),
                ('date', models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)),
                ('draft', models.BooleanField(verbose_name='Черновик', default=True)),
                ('approved', models.BooleanField(verbose_name='Одобрен', default=False)),
                ('finished', models.BooleanField(verbose_name='Закончен', default=False)),
                ('freezed', models.BooleanField(verbose_name='Заморожен', default=False)),
                ('notes', models.TextField(max_length=4096, verbose_name='Заметки к рассказу', blank=True)),
                ('original', models.BooleanField(verbose_name='Оригинальный (не перевод)', default=True)),
                ('summary', models.TextField(verbose_name='Общее описание', max_length=4096)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('vote_up_count', models.PositiveIntegerField(default=0)),
                ('vote_down_count', models.PositiveIntegerField(default=0)),
                ('vote_rating', models.FloatField(default=0)),
                ('authors', models.ManyToManyField(verbose_name='Авторы', blank=True, to=settings.AUTH_USER_MODEL, through='ponyFiction.CoAuthorsStory')),
                ('betas', models.ManyToManyField(related_name='beta_set', verbose_name='Бета-читатели', to=settings.AUTH_USER_MODEL, through='ponyFiction.BetaReading')),
                ('bookmarks', models.ManyToManyField(related_name='bookmarked_story_set', verbose_name='Отложённость', blank=True, to=settings.AUTH_USER_MODEL, through='ponyFiction.Bookmark')),
                ('categories', models.ManyToManyField(verbose_name='Жанры', to='ponyFiction.Category')),
                ('characters', models.ManyToManyField(verbose_name='Персонажи', blank=True, to='ponyFiction.Character')),
                ('classifications', models.ManyToManyField(verbose_name='События', blank=True, to='ponyFiction.Classifier')),
                ('favorites', models.ManyToManyField(related_name='favorites_story_set', verbose_name='Избранность', blank=True, to=settings.AUTH_USER_MODEL, through='ponyFiction.Favorites')),
                ('in_series', models.ManyToManyField(verbose_name='Принадлежность к серии', blank=True, to='ponyFiction.Series', through='ponyFiction.InSeriesPermissions')),
                ('rating', models.ForeignKey(null=True, verbose_name='Рейтинг', to='ponyFiction.Rating')),
            ],
            options={
                'verbose_name': 'рассказ',
                'verbose_name_plural': 'рассказы',
            },
        ),
        migrations.CreateModel(
            name='StoryEditLogItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action', models.SmallIntegerField(choices=[(1, 'опубликовал'), (2, 'отправил в черновики'), (3, 'одобрил'), (4, 'отозвал'), (5, 'отредактировал')])),
                ('json_data', models.TextField(null=True)),
                ('date', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('is_staff', models.BooleanField()),
                ('story', models.ForeignKey(related_name='edit_log', to='ponyFiction.Story')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StoryView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата просмотра', auto_now_add=True)),
                ('author', models.ForeignKey(null=True, verbose_name='Автор просмотра', to=settings.AUTH_USER_MODEL)),
                ('chapter', models.ForeignKey(related_name='chapter_views_set', null=True, verbose_name='Глава рассказа', to='ponyFiction.Chapter')),
                ('story', models.ForeignKey(related_name='story_views_set', null=True, verbose_name='Рассказ', to='ponyFiction.Story')),
            ],
            options={
                'verbose_name': 'просмотр',
                'verbose_name_plural': 'просмотры',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата голосования', auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('ip', models.GenericIPAddressField(verbose_name='IP автора', default='0.0.0.0')),
                ('plus', models.NullBooleanField(verbose_name='Плюс')),
                ('minus', models.NullBooleanField(verbose_name='Минус')),
                ('author', models.ForeignKey(null=True, verbose_name='Автор голоса', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'голос',
                'verbose_name_plural': 'голоса',
            },
        ),
        migrations.AddField(
            model_name='story',
            name='vote',
            field=models.ManyToManyField(verbose_name='Голоса за рассказ', to='ponyFiction.Vote'),
        ),
        migrations.AddField(
            model_name='inseriespermissions',
            name='series',
            field=models.ForeignKey(null=True, verbose_name='Серия', to='ponyFiction.Series'),
        ),
        migrations.AddField(
            model_name='inseriespermissions',
            name='story',
            field=models.ForeignKey(null=True, verbose_name='Рассказ', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='story',
            field=models.ForeignKey(related_name='favorites_story_related_set', null=True, verbose_name='Рассказ', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='comment',
            name='story',
            field=models.ForeignKey(null=True, verbose_name='Отношение к рассказу', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='coauthorsstory',
            name='story',
            field=models.ForeignKey(verbose_name='Рассказ', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='coauthorsseries',
            name='series',
            field=models.ForeignKey(null=True, verbose_name='Серия', to='ponyFiction.Series'),
        ),
        migrations.AddField(
            model_name='character',
            name='group',
            field=models.ForeignKey(null=True, verbose_name='Группа персонажа', to='ponyFiction.CharacterGroup'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='story',
            field=models.ForeignKey(null=True, verbose_name='Отношение к рассказу', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='story',
            field=models.ForeignKey(related_name='bookmarks_related_set', null=True, verbose_name='Рассказ', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='betareading',
            name='story',
            field=models.ForeignKey(null=True, verbose_name='История вычитки', to='ponyFiction.Story'),
        ),
        migrations.AddField(
            model_name='activity',
            name='story',
            field=models.ForeignKey(related_name='story_activity_set', null=True, verbose_name='Рассказ', to='ponyFiction.Story'),
        ),
        migrations.AlterIndexTogether(
            name='storyeditlogitem',
            index_together=set([('story', 'date'), ('is_staff', 'date')]),
        ),
        migrations.AlterIndexTogether(
            name='story',
            index_together=set([('approved', 'draft', 'date'), ('approved', 'draft', 'vote_rating')]),
        ),
    ]
