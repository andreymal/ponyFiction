#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum, Count
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.encoding import is_protected_type
from colorful.fields import RGBColorField

from ponyFiction.filters import filter_html, filtered_html_property
from ponyFiction.filters.base import html_doc_to_string
from ponyFiction.filters.html import footnotes_to_html
from ponyFiction.bl.utils import Resource
from ponyFiction.fields import SeparatedValuesField

from ponyFiction import querymanagers as qm


# disable username validation to allow editing of users with russian symbols in names
username_field = {f.name: f for f in AbstractUser._meta.fields}['username']  # pylint: disable=W0212
username_field.validators = []


class JSONModel(models.Model):
    def to_dict(self, fields=None, exclude_fields=None, relations=None):
        opts = self._meta
        s_opts = self.Serialize
        result = {}

        # select used fields and relations
        if fields is None:
            fields = getattr(s_opts, 'default_fields', None) or opts.get_all_field_names()
        fields = set(fields) - set(exclude_fields or ())

        if isinstance(relations, (tuple, list, set)):
            relations = {x: None for x in relations}
        elif relations is None:
            relations = getattr(s_opts, 'default_relations', None) or {}

        # get values
        for f in opts.local_fields:
            if f.name not in fields:
                continue

            if f.name in relations and f.rel is not None and hasattr(getattr(self, f.name), 'to_dict'):
                # ForeignKey
                item = getattr(self, f.name)
                args = relations.get(f.name)
                if not isinstance(args, dict):
                    args = {'fields': args}
                result[f.name] = item.to_dict(**args)
            else:
                # simple fields and ForeignKey to non-serializable model
                value = f._get_val_from_obj(self)  # pylint: disable=W0212
                if is_protected_type(value):
                    result[f.name] = value
                else:
                    result[f.name] = f.value_to_string(self)

        for f in opts.many_to_many:
            if f.name not in fields:
                continue
            items = []
            for item in getattr(self, f.name).all():
                if f.name in relations and hasattr(item, 'to_dict'):
                    # ManyToMany field item
                    items.append(item.to_dict(relations.get(f.name) if relations else None))
                else:
                    # non-serializable ManyToMany field item
                    items.append(item.pk)
            result[f.name] = items

        # get values of calculated fields
        for name in fields & set(getattr(s_opts, 'properties', ())):
            value = getattr(self, name)
            if is_protected_type(value):
                result[name] = value
            else:
                result[name] = str(value)

        return result

    class Meta:
        abstract = True

    class Serialize:
        pass


class Author(AbstractUser, JSONModel):
    """ Модель автора """

    bio = models.TextField(max_length=2048, blank=True, verbose_name="О себе")
    jabber = models.EmailField(max_length=75, blank=True, verbose_name="Jabber")
    skype = models.CharField(max_length=256, blank=True, verbose_name="Skype ID")
    tabun = models.CharField(max_length=256, blank=True, verbose_name="Табун")
    forum = models.URLField(max_length=200, blank=True, verbose_name="Форум")
    vk = models.CharField(max_length=200, blank=True, verbose_name="VK")
    excluded_categories = SeparatedValuesField(max_length=200, null=True, verbose_name="Скрытые категории")
    detail_view = models.BooleanField(default=False, verbose_name="Детальное отображение рассказов")
    nsfw = models.BooleanField(default=False, verbose_name="NSFW без предупреждения")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

    class Serialize:
        default_fields = {'id', 'username'}

    bio_as_html = filtered_html_property('bio', filter_html)

    def is_authenticated(self):
        return self.is_active

    def get_avatar_url(self):
        url = self.get_tabun_avatar_url()
        if url:
            return url

        return staticfiles_storage.url('images/main/userpic.jpg')

    def get_small_avatar_url(self):
        url = self.get_tabun_avatar_url()
        if url:
            return url.replace('100x100', '24x24')

        return staticfiles_storage.url('images/main/userpic.jpg')

    def get_tabun_avatar_url(self):
        if not self.tabun:
            return

        url = None
        try:
            key = 'tabun_avatar:' + self.tabun
            url = cache.get(key, None)
            if settings.LOAD_TABUN_AVATARS and not url:
                import urllib.request
                from urllib.parse import urljoin
                import random
                import lxml.etree as etree

                profile_url = 'https://tabun.everypony.ru/profile/' + urllib.request.quote(self.tabun)
                req = urllib.request.Request(profile_url)
                req.add_header('User-Agent', 'Mozilla/5.0; ponyFiction')  # for CloudFlare
                data = urllib.request.urlopen(req).read()
                doc = etree.HTML(data.decode('utf-8'))
                links = doc.xpath('//*[contains(@class, "profile-info-about")]//a[contains(@class, "avatar")]/img/@src')
                if links:
                    url = urljoin(profile_url, links[0])
                cache.set(key, url, 300 * (1 + random.random()))
        except Exception:
            if settings.DEBUG:
                import traceback
                traceback.print_exc()

        return url


class CharacterGroup(models.Model):
    """ Модель группы персонажа """

    name = models.CharField(max_length=256, verbose_name="Название группы")
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание группы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа персонажей"
        verbose_name_plural = "Группы персонажей"


class Character(JSONModel):
    """ Модель персонажа """

    description = models.TextField(max_length=4096, blank=True, verbose_name="Биография")
    name = models.CharField(max_length=256, verbose_name="Имя")
    group = models.ForeignKey(CharacterGroup, on_delete=models.CASCADE, null=True, verbose_name="Группа персонажа")

    def __str__(self):
        return self.name

    @property
    def url(self):
        return reverse('search_simple', args=['character', self.id])

    class Meta:
        verbose_name = "персонаж"
        verbose_name_plural = "персонажи"

    class Serialize:
        properties = {'url', 'thumb'}
        default_fields = {'id', 'name', 'url', 'thumb'}


class Category(JSONModel):
    """ Модель жанра """

    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    color = RGBColorField(verbose_name="Цвет ссылки", default="#808080")

    def __str__(self):
        return self.name

    @property
    def url(self):
        return reverse('search_simple', args=['category', self.id])

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    class Serialize:
        properties = {'url'}
        default_fields = {'id', 'name', 'color', 'url'}


class Classifier(JSONModel):
    """ Модель события """

    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"

    class Serialize:
        default_fields = {'id', 'name'}


class Rating(JSONModel):
    """ Модель рейтинга """

    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"

    class Serialize:
        default_fields = {'id', 'name'}


class InSeriesPermissions(models.Model):
    """ Промежуточная модель хранения взаимосвязей рассказов, серий и разрешений на добавления рассказов в серии """

    story = models.ForeignKey('Story', on_delete=models.CASCADE, null=True, verbose_name="Рассказ")
    series = models.ForeignKey('Series', on_delete=models.CASCADE, null=True, verbose_name="Серия")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок рассказов в серии")
    request = models.BooleanField(default=False, verbose_name="Запрос на добавление")
    answer = models.BooleanField(default=False, verbose_name="Ответ на запрос")

    class Meta:
        verbose_name = "добавление в серию"
        verbose_name_plural = "добавления в серию"


class Series(models.Model):
    """ Модель серии """

    authors = models.ManyToManyField(Author, through='CoAuthorsSeries', verbose_name="Авторы")
    cover = models.BooleanField(default=False, verbose_name="Наличие обложки")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    draft = models.BooleanField(default=True, verbose_name="Черновик")
    finished = models.BooleanField(default=False, verbose_name="Оконченность cерии")
    freezed = models.BooleanField(default=False, verbose_name='Статус "заморозки"')
    mark = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка")
    notes = models.TextField(max_length=8192, blank=True, verbose_name="Заметки к серии")
    original = models.BooleanField(default=True, verbose_name="Статус оригинала")
    summary = models.TextField(max_length=8192, verbose_name="Общее описание")
    title = models.CharField(max_length=512, verbose_name="Название")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "серия"
        verbose_name_plural = "серии"

    def __str__(self):
        return self.title


class Story(JSONModel):
    """ Модель рассказа """

    title = models.CharField(max_length=512, verbose_name="Название")
    authors = models.ManyToManyField(Author, blank=True, through='CoAuthorsStory', verbose_name="Авторы")
    betas = models.ManyToManyField(Author, through='BetaReading', related_name="beta_set", verbose_name="Бета-читатели")
    characters = models.ManyToManyField(Character, blank=True, verbose_name='Персонажи')
    categories = models.ManyToManyField(Category, verbose_name='Жанры')
    classifications = models.ManyToManyField(Classifier, blank=True, verbose_name='События')
    cover = models.BooleanField(default=False, verbose_name="Наличие обложки", editable=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    draft = models.BooleanField(default=True, verbose_name="Черновик")
    approved = models.BooleanField(default=False, verbose_name="Одобрен")
    finished = models.BooleanField(default=False, verbose_name="Закончен")
    freezed = models.BooleanField(default=False, verbose_name='Заморожен')
    favorites = models.ManyToManyField(Author, through='Favorites', blank=True, related_name="favorites_story_set", verbose_name="Избранность")
    bookmarks = models.ManyToManyField(Author, through='Bookmark', blank=True, related_name="bookmarked_story_set", verbose_name="Отложённость")
    in_series = models.ManyToManyField(Series, through='InSeriesPermissions', blank=True, verbose_name="Принадлежность к серии")
    notes = models.TextField(max_length=4096, blank=True, verbose_name="Заметки к рассказу")
    original = models.BooleanField(default=True, verbose_name="Оригинальный (не перевод)")
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, verbose_name="Рейтинг")
    summary = models.TextField(max_length=4096, verbose_name="Общее описание")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    words = models.PositiveIntegerField(default=0, editable=settings.DEBUG, verbose_name="Количество слов")
    vote = models.ManyToManyField('Vote', verbose_name="Голоса за рассказ")
    vote_up_count = models.PositiveIntegerField(default = 0, editable = settings.DEBUG)
    vote_down_count = models.PositiveIntegerField(default = 0, editable = settings.DEBUG)
    vote_rating = models.FloatField(default = 0, editable = settings.DEBUG)

    objects = qm.factory(qm.story.MainQS)
    top = qm.factory(qm.story.TopQS)

    bl = Resource('bl.story')

    class Meta:
        verbose_name = "рассказ"
        verbose_name_plural = "рассказы"
        index_together = [
            ['approved', 'draft', 'date'],
            ['approved', 'draft', 'vote_rating'],
        ]

    class Serialize:
        properties = {'published', 'url'}
        default_fields = {
            'id', 'title', 'authors', 'characters', 'categories',
            'date', 'finished', 'freezed', 'original', 'rating', 'summary', 'updated', 'words',
            'vote_total', 'vote_average', 'vote_stddev', 'published', 'url'
        }
        default_relations = {
            'authors': {'id', 'username'},
            'characters': {'id', 'name', 'url', 'thumb'},
            'categories': {'id', 'name', 'url', 'thumb', 'color'},
        }

    def __str__(self):
        return u"[+%s/-%s] %s" % (self.vote_up_count, self.vote_down_count, self.title)

    def get_vote_up_count(self):
        return self.vote.filter(plus=True).count()

    def get_vote_down_count(self):
        return self.vote.filter(minus=True).count()

    @property
    def vote_count(self):
        return self.vote_up_count + self.vote_down_count

    def get_vote_rating(self):
        return self.vote_up_count - self.vote_down_count

    def get_vote_rank(self, invalidate = False):
        key = 'vote_rank_{}'.format(self.pk)
        value = cache.get(key)
        if value is None or invalidate:
            stories = Story.objects.published
            total_count = stories.count()
            rank = stories.extra(where = ['vote_up_count+vote_down_count <= %s'], params = [self.vote_count]).count()
            value = float(rank)/max(total_count, 1)
            cache.set(key, value, 24*3600)
        return value

    def update_rating(self, rating_only = False):
        if not rating_only:
            self.vote_up_count = self.get_vote_up_count()
            self.vote_down_count = self.get_vote_down_count()
        self.vote_rating = self.get_vote_rating()
        self.get_vote_rank(invalidate = True)
        self.save(update_fields = ['vote_up_count', 'vote_down_count', 'vote_rating'])

    def update_words_count(self):
        self.words = self.chapter_set.aggregate(total=Sum('words'))['total']

    def iter_horseshoe_codes(self):
        n = int(round(self.get_vote_rank() * 10))
        k = int(round(float(n*self.vote_up_count)/max(self.vote_count, 1)))
        for i in range(n):
            yield 'lr'[i % 2] + ('g' if i+1 > k else '')

    @property
    def url(self):
        return reverse('story_view', args=[self.id])

    @property
    def published(self):
        return bool(self.approved and not self.draft)

    # Количество просмотров
    @property
    def views(self):
        return self.story_views_set.aggregate(x=Count('author', distinct=True))['x']

    # Дельта количества последних добавленных комментариев с момента посещения юзером рассказа
    def last_comments_by_author(self, author):
        return self.story_activity_set.get(author_id=author).last_comments

    # Проверка авторства
    def editable_by(self, author):
        return author.is_staff or self.is_author(author)

    def deletable_by(self, user):
        return self.is_author(user)

    def is_author(self, author):
        if self.authors.all()._result_cache:  # pylint: disable=W0212
            return author in self.authors.all()
        else:
            return self.authors.filter(id=author.id).exists()

    # Проверка возможности публикации
    @property
    def publishable(self):
        return True if self.words > settings.PUBLISH_SIZE_LIMIT else False

    @property
    def nsfw(self):
        return True if self.rating_id in settings.NSFW_RATING_IDS else False

    summary_as_html = filtered_html_property('summary', filter_html)
    notes_as_html = filtered_html_property('notes', filter_html)

    def list_downloads(self):
        from .downloads import list_formats
        downloads = []
        for f in list_formats():
            downloads.append({
                'format': f,
                'url': f.url(self),
            })
        return downloads


class Chapter(models.Model):
    """ Модель главы """

    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE, verbose_name="Отношение к рассказу")
    mark = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка")
    notes = models.TextField(blank=True, verbose_name="Заметки к главе")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок глав в рассказу")
    title = models.CharField(max_length=512, verbose_name="Название")
    text = models.TextField(blank=True, verbose_name="Текст главы")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    words = models.IntegerField(default=0, verbose_name="Количество слов в главе")

    bl = Resource('bl.chapter')

    class Meta:
        verbose_name = "глава"
        verbose_name_plural = "главы"

    def __str__(self):
        return '[%s / %s] %s' % (self.id, self.order, self.title)

    def get_absolute_url(self):
        return reverse('chapter_view_single', kwargs=dict(story_id=self.story_id, chapter_order=self.order))

    def get_prev_chapter(self):
        try:
            return self.story.chapter_set.filter(order__lt=self.order).latest('order')
        except Chapter.DoesNotExist:
            return None

    def get_next_chapter(self):
        try:
            return self.story.chapter_set.filter(order__gt=self.order)[0:1].get()
        except Chapter.DoesNotExist:
            return None

    @property
    def published(self):
        return self.story.published

    # Количество просмотров
    @property
    def views(self):
        return self.chapter_views_set.values('author').annotate(Count('author')).count()

    def editable_by(self, author):
        return self.story.editable_by(author)

    notes_as_html = filtered_html_property('notes', filter_html)

    @property
    def text_as_html(self):
        try:
            doc = self.get_filtered_chapter_text()
            doc = footnotes_to_html(doc)
            return mark_safe(html_doc_to_string(doc))
        except:
            if settings.DEBUG:
                import traceback
                return traceback.format_exc()
            return "#ERROR#"

    def get_filtered_chapter_text(self):
        return filter_html(
            self.text,
            tags=settings.CHAPTER_ALLOWED_TAGS,
            attributes=settings.CHAPTER_ALLOWED_ATTRIBUTES,
        )


class CoAuthorsStory(models.Model):
    """ Промежуточная модель хранения взаимосвязей авторства рассказов (включая соавторов) """

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name="Рассказ")
    approved = models.BooleanField(default=False, verbose_name="Подтверждение")

    def __str__(self):
        return '%s (%s)' % (self.author.username, self.story.title)


class CoAuthorsSeries(models.Model):
    """ Промежуточная модель хранения взаимосвязей авторства серий (включая соавторов) """

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, verbose_name="Автор")
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, verbose_name="Серия")
    approved = models.BooleanField(default=False, verbose_name="Подтверждение")

    def __str__(self):
        return '%s (%s)' % (self.author.username, self.series.title)


class BetaReading(models.Model):
    """ Промежуточная модель хранения взаимосвязей рассказов, бета-читателей и результатов вычитки """

    beta = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, verbose_name="Бета")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True, verbose_name="История вычитки")
    checked = models.BooleanField(default=False, verbose_name="Вычитано бетой")

    def __str__(self):
        if self.checked:
            return "%s -> %s [OK]" % (self.beta.username, self.story.title)
        else:
            return "%s -> %s [?]" % (self.beta.username, self.story.title)

    class Meta:
        verbose_name = "вычитка"
        verbose_name_plural = "вычитки"


class Comment(models.Model):
    """ Модель комментария """

    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор комментария")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE, verbose_name="Отношение к рассказу")
    text = models.TextField(verbose_name="Текст комментария")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    ip = models.GenericIPAddressField(default='0.0.0.0', verbose_name="IP комментатора")

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return self.text

    def editable_by(self, author):
        return author.is_staff

    @property
    def brief_text(self):
        text = self.text
        if len(text) > settings.BRIEF_COMMENT_LENGTH:
            text = text[:settings.BRIEF_COMMENT_LENGTH] + '...'
        return text

    text_as_html = filtered_html_property('text', filter_html)
    brief_text_as_html = filtered_html_property('brief_text', filter_html)

    def get_absolute_url(self):
        return '%s#%s' % (self.story.url, self.get_html_id())

    def get_html_id(self):
        return 'comment_%s' % self.id


class Vote(models.Model):
    """ Модель голосований """

    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор голоса")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    ip = models.GenericIPAddressField(default='0.0.0.0', verbose_name="IP автора")
    plus = models.NullBooleanField(null=True, verbose_name="Плюс")
    minus = models.NullBooleanField(null=True, verbose_name="Минус")

    class Meta:
        verbose_name = "голос"
        verbose_name_plural = "голоса"


class Favorites(models.Model):
    """ Модель избранного """

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, verbose_name="Автор")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="favorites_story_related_set", null=True, verbose_name="Рассказ")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в избранное")

    class Meta:
        verbose_name = "избранное"
        verbose_name_plural = "избранное"

    def __str__(self):
        return "%s: %s [%s]" % (self.author.username, self.story.title, self.date)


class Bookmark(models.Model):
    """ Модель закладок """

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, verbose_name="Автор")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="bookmarks_related_set", null=True, verbose_name="Рассказ")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в список для прочтения")

    class Meta:
        verbose_name = "закладка рассказа"
        verbose_name_plural = "закладки рассказов"

    def __str__(self):
        return "%s | %s" % (self.author.username, self.story.title)


class StoryView(models.Model):
    """ Модель просмотров """
    # NOTE: Будет расширена и переименована для серий
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор просмотра")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="story_views_set", null=True, verbose_name="Рассказ")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="chapter_views_set", null=True, verbose_name="Глава рассказа")

    class Meta:
        verbose_name = "просмотр"
        verbose_name_plural = "просмотры"

    def __str__(self):
        return "%s: %s" % (self.author.username, self.story.title)


class Activity(models.Model):
    """ Модель отслеживания активности """

    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор просмотра")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата последнего просмотра автором")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="story_activity_set", null=True, verbose_name="Рассказ")
    last_views = models.IntegerField(default=0, verbose_name="Последнее количество просмотров")
    last_comments = models.IntegerField(default=0, verbose_name="Последнее количество комментариев")
    last_vote_up = models.IntegerField(default=0, verbose_name="Последнее количество голосов 'За'")
    last_vote_down = models.IntegerField(default=0, verbose_name="Последнее количество голосов 'Против'")

    class Meta:
        verbose_name = "активность"
        verbose_name_plural = "активность"

    def __str__(self):
        return "%s: %s [v:%s c:%s (+):%s (-):%s]" % (self.author.username, self.story.title, self.last_views, self.last_comments, self.last_vote_up, self.last_vote_down)


class StoryEditLogItem(models.Model):
    class Actions:
        Publish = 1
        Unpublish = 2
        Approve = 3
        Unapprove = 4
        Edit = 5

        action_verbs = {
            Publish: 'опубликовал',
            Unpublish: 'отправил в черновики',
            Approve: 'одобрил',
            Unapprove: 'отозвал',
            Edit: 'отредактировал',
        }

    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='edit_log')
    action = models.SmallIntegerField(choices=Actions.action_verbs.items())
    json_data = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    is_staff = models.BooleanField()

    def action_verb(self):
        return self.Actions.action_verbs[self.action]

    @property
    def data(self):
        return json.loads(self.json_data)

    @data.setter
    def data(self, value):
        def default(o):
            if isinstance(o, models.Model):
                return o.id
            elif isinstance(o, models.query.QuerySet):
                return list(o)
        self.json_data = json.dumps(
            value,
            ensure_ascii=False,
            default=default,
        )

    @classmethod
    def create(cls, data=None, **kw):
        obj = cls(**kw)
        obj.is_staff = kw['user'].is_staff
        if data is not None:
            obj.data = data
        obj.save()
        return obj

    class Meta:
        index_together = [
            ['story', 'date'],
            ['is_staff', 'date'],
        ]


class StaticPage(models.Model):
    name = models.CharField(max_length=128, db_index=True, verbose_name="Название")
    title = models.CharField(max_length=255, verbose_name="Заголовок страницы")
    content = models.TextField(verbose_name="Содержимое")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "страницы"

    def __str__(self):
        return self.title


class NewsItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок новости")
    text = models.TextField(blank=True, verbose_name="Текст новости")
    visible = models.BooleanField(default=False, verbose_name="Опубликована")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    bl = Resource('bl.newsitem')

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"

    def __str__(self):
        return self.title
