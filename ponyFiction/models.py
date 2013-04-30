# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Sum, F
from django.utils.safestring import mark_safe
from ponyFiction.fields import SeparatedValuesField
from ponyFiction.filters import filter_html, filtered_html_property
from ponyFiction.filters.base import html_doc_to_string
from ponyFiction.filters.html import footnotes_to_html

class Author(AbstractUser):
    """ Модель автора """
    
    bio = models.TextField(max_length=2048, blank=True, verbose_name="О себе")
    jabber = models.EmailField(max_length=75, blank=True, verbose_name="Jabber")
    skype = models.CharField(max_length=256, blank=True, verbose_name="Skype ID")
    tabun = models.CharField(max_length=256, blank=True, verbose_name="Табун")
    forum = models.URLField(max_length=200, blank=True, verbose_name="Форум")
    vk = models.URLField(max_length=200, blank=True, verbose_name="VK")
    approved = models.BooleanField(default=False, verbose_name="Проверенный автор")
    excluded_categories = SeparatedValuesField(max_length=200, null=True, verbose_name="Скрытые категории")
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"
        
    bio_as_html = filtered_html_property('bio', filter_html)

class CharacterGroup(models.Model):
    """ Модель группы персонажа """

    name = models.CharField(max_length=256, verbose_name="Название группы")
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание группы")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "Группа персонажей"
        verbose_name_plural = "Группы персонажей"
        
class Character(models.Model):
    """ Модель персонажа """
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Биография")
    name = models.CharField(max_length=256, verbose_name="Имя")
    group = models.ForeignKey(CharacterGroup, null=True, verbose_name="Группа персонажа")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "персонаж"
        verbose_name_plural = "персонажи"

class Category(models.Model):
    """ Модель категории """
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

class Classifier(models.Model):
    """ Модель классификатора """
   
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "классификатор"
        verbose_name_plural = "классификаторы"

class Rating(models.Model):
    """ Модель рейтинга """
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    warning = models.TextField(max_length=2048, blank=True, verbose_name="Предупреждение")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"
    
class BetaReading(models.Model):
    """ Промежуточная модель хранения взаимосвязей рассказов, бета-читателей и результатов вычитки """

    beta = models.ForeignKey(Author, null=True, verbose_name="Бета")
    story = models.ForeignKey('Story', null=True, verbose_name="История вичитки")
    checked = models.BooleanField(default=False, verbose_name="Вычитано бетой")

    def __unicode__(self):
        if self.checked:
            return "%s -> %s [OK]" % self.name
        else:
            return "%s -> %s [?]" % self.name

    class Meta:
        verbose_name = "вычитка"
        verbose_name_plural = "вычитки"


class InSeriesPermissions(models.Model):
    """ Промежуточная модель хранения взаимосвязей рассказов, серий и разрешений на добавления рассказов в серии """
    
    story = models.ForeignKey('Story', null=True, verbose_name="Рассказ")
    series = models.ForeignKey('Series', null=True, verbose_name="Серия")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок рассказов в серии")
    request = models.BooleanField(default=False, verbose_name="Запрос на добавление")
    answer = models.BooleanField(default=False, verbose_name="Ответ на запрос")

    class Meta:
        verbose_name = "добавление в серию"
        verbose_name_plural = "добавления в серию"

class CoAuthorsStory(models.Model):
    """ Промежуточная модель хранения взаимосвязей авторства рассказов (включая соавторов) """

    author = models.ForeignKey(Author, verbose_name="Автор")
    story = models.ForeignKey('Story', verbose_name="Рассказ")
    approved = models.BooleanField(default=False, verbose_name="Подтверждение")
    
    def __unicode__(self):
        return '%s %s' % (self.author.username, self.story.title)
    
class CoAuthorsSeries(models.Model):
    """ Промежуточная модель хранения взаимосвязей авторства серий (включая соавторов) """
    
    author = models.ForeignKey(Author, null=True, verbose_name="Автор")
    series = models.ForeignKey('Series', null=True, verbose_name="Серия")
    approved = models.BooleanField(default=False, verbose_name="Подтверждение")
    
    def __unicode__(self):
        return '%s %s' % (self.author.username, self.series.title)

class Series(models.Model):
    """ Модель серии """
   
    authors = models.ManyToManyField(Author, through='CoAuthorsSeries', verbose_name=u"Авторы")
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

    def __unicode__(self):
        return self.title

    
class StoryQuerySet(models.query.QuerySet):
    from datetime import datetime, timedelta
    last = datetime.now() - timedelta(weeks=1)
    
    @property
    def published(self):
        return self.filter(draft=False, approved=True)
    
    @property
    def submitted(self):
        return self.filter(draft=False, approved=False)
    
    @property
    def good(self):
        return self.annotate(votes_up=Count('vote__plus'), votes_down=Count('vote__minus'), votes_all=Count('vote')).exclude(votes_all__gte=20, votes_down__gte=F('votes_all') * 0.5)
    
    @property
    def last_week(self):
        return self.filter(date__gte=self.last)
    
    def accessible(self, user):
        from django.db.models import Q
        qs = self.filter(Q(date__gte=self.last)|Q(draft=False, approved=True))
        if user.is_anonymous():
            return qs
        else:
            return qs.exclude(categories__in=user.excluded_categories)
    
class StoryManager(models.Manager):
    def get_query_set(self):
        return StoryQuerySet(self.model, using=self._db)

    @property
    def published(self):
        return self.get_query_set().published
    
    @property
    def submitted(self):
        return self.get_query_set().submitted
    
    @property
    def good(self):
        return self.get_query_set().good
    
    @property
    def last_week(self):
        return self.get_query_set().last_week
    
    def accessible(self, user):
        return self.get_query_set().accessible(user)
    
class Story (models.Model):
    """ Модель рассказа """
    
    authors = models.ManyToManyField(Author, null=True, through='CoAuthorsStory', verbose_name=u"Авторы")
    betas = models.ManyToManyField(Author, through='BetaReading', related_name="beta_set", verbose_name=u"Бета-читатели")
    characters = models.ManyToManyField(Character, blank=True, null=True, verbose_name='Персонажи')
    categories = models.ManyToManyField(Category, verbose_name='Жанры')
    classifications = models.ManyToManyField(Classifier, blank=True, null=True, verbose_name='События')
    cover = models.BooleanField(default=False, verbose_name="Наличие обложки")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    draft = models.BooleanField(default=True, verbose_name="Черновик")
    approved = models.BooleanField(default=False, verbose_name="Статус одобрения")
    finished = models.BooleanField(default=False, verbose_name="Оконченность рассказа")
    freezed = models.BooleanField(default=False, verbose_name='Статус "заморозки"')
    favorites = models.ManyToManyField(Author, through='Favorites', blank=True, null=True, related_name="favorites_story_set", verbose_name="Избранность")
    bookmarks = models.ManyToManyField(Author, through='Bookmark', blank=True, null=True, related_name="bookmarked_story_set", verbose_name="Отложённость")
    in_series = models.ManyToManyField(Series, through='InSeriesPermissions', blank=True, null=True, verbose_name="Принадлежность к серии")
    mark = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка")
    notes = models.TextField(max_length=4096, blank=True, verbose_name="Заметки к рассказу")
    original = models.BooleanField(default=True, verbose_name="Статус оригинала")
    rating = models.ForeignKey(Rating, null=True, verbose_name="Рейтинг")
    summary = models.TextField(max_length=4096, verbose_name="Общее описание")
    title = models.CharField(max_length=512, verbose_name="Название")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    vote = models.ManyToManyField('Vote', null=True, verbose_name="Голоса за рассказ")

    objects = StoryManager()
    
    class Meta:
        verbose_name = "рассказ"
        verbose_name_plural = "рассказы"

    def __unicode__(self):
        return u"[+%s/-%s] %s" % (self.vote_up_count, self.vote_down_count, self.title)
    
    @property
    def vote_up_count(self):
        return self.vote.filter(plus=True).count()
    
    @property
    def vote_down_count(self):
        return self.vote.filter(minus=True).count()

    # Количество просмотров
    @property
    def views(self):
        return self.story_views_set.values('author').annotate(Count('author')).count()
    
    # Количество слов
    @property
    def words(self):
        return self.chapter_set.aggregate(Sum('words'))['words__sum']
    
    # Дельта количества последних добавленных комментариев с момента посещения юзером рассказа
    def last_comments_by_author(self, author):
        return self.story_activity_set.get(author_id=author).last_comments
    
    # Проверка авторства
    def editable_by(self, author):
        return author.is_staff or self.authors.filter(id=author.id).exists()
    
    # Проверка возможности публикации
    @property
    def publishable(self):
        return True if self.words > settings['PUBLISH_SIZE_LIMIT'] else False
    
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

class Chapter (models.Model):
    """ Модель главы """
    
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    draft = models.BooleanField(default=True, verbose_name="Черновик")
    story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE, verbose_name="Отношение к рассказу")
    mark = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка")
    notes = models.TextField(blank=True, verbose_name="Заметки к главе")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок глав в рассказу")
    title = models.CharField(max_length=512, verbose_name="Название")
    text = models.TextField(blank=True, verbose_name="Текст главы")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    words = models.IntegerField(default=0, verbose_name="Количество слов в главе")
    
    class Meta:
        verbose_name = "глава"
        verbose_name_plural = "главы"
    
    def __unicode__(self):
        return '[%s / %s] %s' % (self.id, self.order, self.title)

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
        
    # Количество просмотров
    @property
    def views(self):
        return self.chapter_views_set.values('author').annotate(Count('author')).count()

    def editable_by(self, author):
        return self.story.editable_by(author)
    
    notes_as_html = filtered_html_property('notes', filter_html)
    
    @property
    def text_as_html(self):
        doc = self.get_filtered_chapter_text()
        doc = footnotes_to_html(doc)  
        return mark_safe(html_doc_to_string(doc)) 
    
    def get_filtered_chapter_text(self):
        return filter_html(
            self.text,
            tags = settings.CHAPTER_ALLOWED_TAGS,
            attributes = settings.CHAPTER_ALLOWED_ATTRIBUTES,
        )
    
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
    
    def __unicode__(self):
        return self.text
    
    text_as_html = filtered_html_property('text', filter_html)

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
    
    def __unicode__(self):
        if self.plus is not None:
            return "%s [+] story '%s'" % (self.author.username, self.story_set.all()[0].title)
        if self.minus is not None:
            return "%s [-] story '%s'" % (self.author.username, self.story_set.all()[0].title)
    
class Favorites(models.Model):
    """ Модель избранного """
    
    author = models.ForeignKey(Author, null=True, verbose_name="Автор")
    story = models.ForeignKey('Story', related_name="favorites_story_related_set", null=True, verbose_name="Рассказ")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в избранное")

    class Meta:
        verbose_name = "избранное"
        verbose_name_plural = "избранное"
    
    def __unicode__(self):
        return "%s: %s [%s]" % (self.author.username, self.story.title, self.date)    

class Bookmark(models.Model):
    """ Модель закладок """
    
    author = models.ForeignKey(Author, null=True, verbose_name="Автор")
    story = models.ForeignKey(Story, related_name="bookmarks_related_set", null=True, verbose_name="Рассказ")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в список для прочтения")
    
    class Meta:
        verbose_name = "закладка рассказа"
        verbose_name_plural = "закладки рассказов"
    
    def __unicode__(self):
            return u"%s | %s" % (self.author.username, self.story.title)


class StoryView(models.Model):
    """ Модель просмотров """
    # NOTE: Будет расширена и переименована для серий
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор просмотра")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")
    story = models.ForeignKey(Story, related_name="story_views_set", null=True, verbose_name="Рассказ")
    chapter = models.ForeignKey(Chapter, related_name="chapter_views_set", null=True, verbose_name="Глава рассказа")
    
    class Meta:
        verbose_name = "просмотр"
        verbose_name_plural = "просмотры"
    
    def __unicode__(self):
        return "%s: %s" % (self.author.username, self.story.title)


class Activity(models.Model):
    """ Модель отслеживания активности """
    
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор просмотра")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата последнего просмотра автором")
    story = models.ForeignKey(Story, related_name="story_activity_set", null=True, verbose_name="Рассказ")
    last_views = models.IntegerField(default=0, verbose_name="Последнее количество просмотров")
    last_comments = models.IntegerField(default=0, verbose_name="Последнее количество комментариев")
    last_vote_up = models.IntegerField(default=0, verbose_name="Последнее количество голосов 'За'")
    last_vote_down = models.IntegerField(default=0, verbose_name="Последнее количество голосов 'Против'")
    
    class Meta:
        verbose_name = "активность"
        verbose_name_plural = "активность"
    
    def __unicode__(self):
        return "%s: %s [v:%s c:%s (+):%s (-):%s]" % (self.author.username, self.story.title, self.last_views, self.last_comments, self.last_vote_up, self.last_vote_down)
