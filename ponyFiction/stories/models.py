# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager

class Author(User):
# Модель автора    

    # temporary old user id
    old_id = models.IntegerField(null=True)
    
    bio = models.TextField(max_length=2048, blank=True, verbose_name="О себе")
    jabber = models.EmailField(max_length=75, blank=True, verbose_name="Jabber")
    skype = models.CharField(max_length=256, blank=True, verbose_name="Skype ID")
    tabun = models.CharField(max_length=256, blank=True, verbose_name="Табун")
    forum = models.URLField(max_length=200, blank=True, verbose_name="Форум")
    vk = models.URLField(max_length=200, blank=True, verbose_name="VK")
    
    # Используем UserManager для доступа к методам User 
    objects = UserManager()
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

class CharacterGroup(models.Model):
# Модель группы персонажа

    name = models.CharField(max_length=256, verbose_name="Название группы")
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание группы")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "Группа персонажей"
        verbose_name_plural = "Группы персонажей"
        
class Character(models.Model):
# Модель персонажа

    old_id = models.IntegerField(null=True)
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Биография")
    name = models.CharField(max_length=256, verbose_name="Имя")
    group = models.ForeignKey(CharacterGroup, null=True, verbose_name="Группа персонажа")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "персонаж"
        verbose_name_plural = "персонажи"

class Category(models.Model):
# Модель категории

    old_id = models.IntegerField(null=True)
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

class Classifier(models.Model):
# Модель классификатора

    old_id = models.IntegerField(null=True)
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "классификатор"
        verbose_name_plural = "классификаторы"

class Size(models.Model):
# Модель размера

    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "размер"
        verbose_name_plural = "размеры"

class Rating(models.Model):
# Модель рейтинга

    old_id = models.IntegerField(null=True)
    
    description = models.TextField(max_length=4096, blank=True, verbose_name="Описание")
    name = models.CharField(max_length=256, verbose_name="Название")
    warning = models.TextField(max_length=2048, blank=True, verbose_name="Предупреждение")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"
    
class BetaReading(models.Model):
# Промежуточная модель хранения взаимосвязей историй, бета-читателей и результатов вычитки

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
# Промежуточная модель хранения взаимосвязей историй, серий и разрешений на добавления историй в серии
    story = models.ForeignKey('Story', null=True, verbose_name="История")
    series = models.ForeignKey('Series', null=True, verbose_name="Серия")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок историй в серии")
    request = models.BooleanField(default=False, verbose_name="Запрос на добавление")
    answer = models.BooleanField(default=False, verbose_name="Ответ на запрос")

    class Meta:
        verbose_name = "добавление в серию"
        verbose_name_plural = "добавления в серию"

class CoAuthorsStory(models.Model):
    author = models.ForeignKey(Author, verbose_name="Автор")
    story = models.ForeignKey('Story', verbose_name="История")
    approved = models.BooleanField(default=False, verbose_name="Подтверждение")
    
    def __unicode__(self):
        return '%s %s' % (self.author.username, self.story.title)
    
class CoAuthorsSeries(models.Model):
    author = models.ForeignKey(Author, null=True, verbose_name="Автор")
    series = models.ForeignKey('Series', null=True, verbose_name="Серия")
    approved = models.BooleanField(default=False, verbose_name="Подтверждение")
    
    def __unicode__(self):
        return '%s %s' % (self.author.username, self.series.title)

class Series(models.Model):
# Модель серии
    
    # temporary old series id
    old_id = models.IntegerField(null=True)
    
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

class Story (models.Model):
# Модель истории
    
    # temporary old story id
    old_id = models.IntegerField(null=True)
    
    authors = models.ManyToManyField(Author, null=True, through='CoAuthorsStory', verbose_name=u"Авторы")
    betas = models.ManyToManyField(Author, through='BetaReading', related_name="beta_set", verbose_name=u"Бета-читатели")
    characters = models.ManyToManyField(Character, blank=True, null=True, verbose_name='Персонажи')
    categories = models.ManyToManyField(Category, verbose_name='Жанры')
    classifications = models.ManyToManyField(Classifier, blank=True, null=True, verbose_name='События')
    cover = models.BooleanField(default=False, verbose_name="Наличие обложки")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    draft = models.BooleanField(default=True, verbose_name="Черновик")
    finished = models.BooleanField(default=False, verbose_name="Оконченность истории")
    freezed = models.BooleanField(default=False, verbose_name='Статус "заморозки"')
    favorites = models.ManyToManyField(Author, through='Favorites', blank=True, null=True, related_name="favorites_story_set", verbose_name="Избранность")
    deferred = models.ManyToManyField(Author, through='Deferred', blank=True, null=True, related_name="deferred_story_set", verbose_name="Отложённость")
    in_series = models.ManyToManyField(Series, through='InSeriesPermissions', blank=True, null=True, verbose_name="Принадлежность к серии")
    mark = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка")
    notes = models.TextField(max_length=4096, blank=True, verbose_name="Заметки к истории")
    original = models.BooleanField(default=True, verbose_name="Статус оригинала")
    rating = models.ForeignKey(Rating, null=True, verbose_name="Рейтинг")
    summary = models.TextField(max_length=4096, verbose_name="Общее описание")
    size = models.ForeignKey(Size, null=True, verbose_name="Размер")
    title = models.CharField(max_length=512, verbose_name="Название")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    vote = models.ManyToManyField('Vote', null=True, verbose_name="Голоса за историю")
    words = models.IntegerField(default=0, verbose_name="Количество слов в истории")

    class Meta:
        verbose_name = "история"
        verbose_name_plural = "истории"

    def __unicode__(self):
        return self.title
    
    def vote_up_count(self):
        return self.vote.filter(direction = True).count()
    
    def vote_down_count(self):
        return self.vote.filter(direction = False).count()   

class Chapter (models.Model):
# Модель главы
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    draft = models.BooleanField(default=True, verbose_name="Черновик")   
    in_story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE, verbose_name="Отношение к истории")
    mark = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка")
    notes = models.TextField(blank=True, verbose_name="Заметки к главе")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Порядок глав в истории")
    title = models.CharField(max_length=512, verbose_name="Название")
    text = models.TextField(blank=True, verbose_name="Текст главы")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    words = models.IntegerField(default=0, verbose_name="Количество слов в главе")
    
    class Meta:
        verbose_name = "глава"
        verbose_name_plural = "главы"
    
    def __unicode__(self):
        return '[%s / %s] %s (%s)' % (self.id, self.order, self.title, self.in_story.title)

    def get_prev_chapter(self):
        try:
            return self.in_story.chapter_set.filter(order__lt = self.order).latest('order')
        except Chapter.DoesNotExist:
            return None

    def get_next_chapter(self):
        try:
            return self.in_story.chapter_set.filter(order__gt = self.order)[0:1].get()
        except Chapter.DoesNotExist:
            return None

class Comment(models.Model):
# Модель комментария
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор комментария")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    in_story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE, verbose_name="Отношение к истории")
    text = models.TextField(verbose_name="Текст комментария")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    ip = models.GenericIPAddressField(default='0.0.0.0', verbose_name="IP комментатора")
    
    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
    
    def __unicode__(self):
        return self.text

class Vote(models.Model):
# Модель голосований
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, verbose_name="Автор голоса")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    ip = models.GenericIPAddressField(default='0.0.0.0', verbose_name="IP автора")
    direction = models.BooleanField(default=True, verbose_name="Направление")
    
    class Meta:
        verbose_name = "голос"
        verbose_name_plural = "голоса"
    
    def __unicode__(self):
        if self.direction:
            return "%s [+] story '%s'" % (self.author.username, self.story_set.all()[0].title)
        else:
            return "%s [-] story '%s'" % (self.author.username, self.story_set.all()[0].title)
    
class Favorites(models.Model):
    author = models.ForeignKey(Author, null=True, verbose_name="Автор")
    story = models.ForeignKey('Story', related_name="favorites_set", null=True, verbose_name="История")
    comment = models.TextField(verbose_name="Текст комментария")

class Deferred(models.Model):
    author = models.ForeignKey(Author, null=True, verbose_name="Автор")
    story = models.ForeignKey('Story', related_name="deferred_set", null=True, verbose_name="История")
    comment = models.TextField(verbose_name="Текст комментария")

"""
TODO: (для меня)
Сделать модель Activity (отслеживание активности)
Сделать модель View (просмотр)
"""