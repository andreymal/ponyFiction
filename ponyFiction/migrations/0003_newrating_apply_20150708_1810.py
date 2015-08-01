# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from statistics import mean, pstdev

from django.db import migrations


def convert_votes(apps, schema_editor):
    Vote = apps.get_model('ponyFiction', 'Vote')
    Vote.objects.filter(plus=True).update(vote_value=5)
    Vote.objects.filter(minus=True).update(vote_value=1)


def update_stories_votes(apps, schema_editor):
    Vote = apps.get_model('ponyFiction', 'Vote')
    Story = apps.get_model('ponyFiction', 'Story')
    # так как джанга после трёх часов любви так и не согласилась мне выдывать story.vote, приходится дичайше костылять
    stories = {}

    for vote in Vote.objects.all():
        story_id = vote.story_set.all().values_list('id', flat=True)[0]
        if story_id not in stories:
            stories[story_id] = []
        stories[story_id].append(vote.vote_value)
        vote.story_id = story_id
        vote.save()

    for story in Story.objects.all():
        if story.id not in stories:
            continue
        story.vote_total = len(stories[story.id])
        m = mean(stories[story.id])
        story.vote_average = m
        story.vote_stddev = pstdev(stories[story.id], m)
        story.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0002_newrating_20150708_1807'),
    ]

    operations = [
        migrations.RunPython(convert_votes),
        migrations.RunPython(update_stories_votes),

        migrations.AlterIndexTogether(
            name='story',
            index_together=set([('approved', 'draft', 'date'), ('approved', 'draft', 'vote_average', 'vote_stddev')]),
        ),
        migrations.RemoveField(
            model_name='vote',
            name='minus',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='plus',
        ),
        migrations.RemoveField(
            model_name='story',
            name='vote_down_count',
        ),
        migrations.RemoveField(
            model_name='story',
            name='vote_up_count',
        ),
        migrations.RemoveField(
            model_name='story',
            name='vote_rating',
        ),
        migrations.RemoveField(
            model_name='story',
            name='vote',
        ),
    ]
