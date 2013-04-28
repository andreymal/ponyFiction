from django.db.models.signals import pre_save
from ponyFiction.models import Chapter, Story, Author, Activity
from django.dispatch import Signal, receiver

story_viewed = Signal(providing_args=['story'])

@receiver(pre_save, sender=Chapter)
def update_chapter_word_count(sender, instance, **kw):
    from django.template import defaultfilters as filters
    instance.words = filters.wordcount(filters.striptags(instance.text))

@receiver(pre_save, sender=Chapter)
def update_story_update_time(sender, instance, **kw):
    story = Story.objects.get(id = instance.story_id)
    story.save()
    
@receiver(story_viewed, sender=Author)
def story_activity_save(sender, instance, **kwargs):
    if instance.is_anonymous():
        return
    story = kwargs['story']
    comments_count = kwargs['comments_count']
    activity = Activity.objects.get_or_create(author_id=instance.id, story=story)[0]
    activity.last_views = story.views
    activity.last_comments = comments_count
    activity.last_vote_up = story.vote_up_count
    activity.last_vote_down = story.vote_down_count
    activity.save()