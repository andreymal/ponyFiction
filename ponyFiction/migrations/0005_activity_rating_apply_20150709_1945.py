# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from statistics import mean, pstdev

from django.db import migrations


def update_activity_votes(apps, schema_editor):
    Activity = apps.get_model('ponyFiction', 'Activity')
    for act in Activity.objects.all():
        votes = ([5] * act.last_vote_up) + ([1] * act.last_vote_down)
        if votes:
            m = mean(votes)
            act.last_vote_average = m
            act.last_vote_stddev = pstdev(votes, m)
            act.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0004_activity_rating_20150709_1944'),
    ]

    operations = [
        migrations.RunPython(update_activity_votes),

        migrations.RemoveField(
            model_name='activity',
            name='last_vote_down',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='last_vote_up',
        ),
    ]
