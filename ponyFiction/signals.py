from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import Signal, receiver

from ponyFiction.models import Chapter, Story, Author, Activity, StoryView, Vote, Comment
from ponyFiction import tasks


story_visited = Signal(providing_args=['story'])
story_viewed = Signal(providing_args=['story', 'chapter'])


@receiver(pre_save, sender=Chapter)
def update_chapter_word_count(sender, instance, **kw):
    from django.template import defaultfilters as filters
    instance.words = filters.wordcount(filters.striptags(instance.text))


@receiver(post_save, sender=Chapter)
def update_story_update_time(sender, instance, **kw):
    story = Story.objects.get(id=instance.story_id)
    story.save(update_fields=['updated'])


@receiver(story_visited, sender=Author)
def story_activity_save(sender, instance, **kwargs):
    if not instance.is_authenticated():
        return
    story = kwargs['story']
    comments_count = kwargs['comments_count']
    activity = Activity.objects.get_or_create(author_id=instance.id, story=story)[0]
    activity.last_views = story.views
    activity.last_comments = comments_count
    activity.last_vote_up = story.vote_up_count
    activity.last_vote_down = story.vote_down_count
    activity.save()


@receiver(story_viewed, sender=Author)
def story_views_save(sender, instance, **kwargs):
    if not instance.is_authenticated():
        return
    story = kwargs['story']
    chapter = kwargs['chapter']
    view = StoryView.objects.create()
    view.author = instance
    view.story_id = story.id
    view.chapter = chapter
    view.save()


@receiver(post_save, sender=Vote)
def votes_update(sender, instance, rating_only = False, **kw):
    for story in instance.story_set.all():
        story.update_rating(rating_only = rating_only)


@receiver(post_save, sender=Story)
def sphinx_update_story(sender, instance, **kw):
    if not kw.get('update_fields'):
        return  # см. views/story.py
    tasks.sphinx_update_story.delay(instance.id, list(kw.get('update_fields')))


@receiver(post_save, sender=Chapter)
def sphinx_update_chapter(sender, instance, **kw):
    tasks.sphinx_update_chapter.delay(instance.id)


@receiver(post_save, sender=Comment)
def sphinx_update_comments_count(sender, instance, **kw):
    tasks.sphinx_update_comments_count.delay(instance.story_id)


@receiver(post_delete, sender=Comment)
def sphinx_delete_comments_count(sender, instance, **kw):
    tasks.sphinx_update_comments_count.delay(instance.story_id)


@receiver(post_delete, sender=Story)
def sphinx_delete_story(sender, instance, **kw):
    tasks.sphinx_delete_story.delay(instance.id)


@receiver(post_delete, sender=Chapter)
def sphinx_delete_chapter(sender, instance, **kw):
    tasks.sphinx_delete_chapter.delay(instance.story_id, instance.id)
