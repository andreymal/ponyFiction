# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_words(apps, schema_editor):
    Story = apps.get_model('ponyFiction', 'Story')
    for story in Story.objects.all().only('id').iterator():
        story.words = story.chapter_set.aggregate(models.Sum('words'))['words__sum'] or 0
        story.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0005_activity_rating_apply_20150709_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='words',
            field=models.PositiveIntegerField(verbose_name='Количество слов', default=0),
        ),

        migrations.RunPython(update_words)
    ]
