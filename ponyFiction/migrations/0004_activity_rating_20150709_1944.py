# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ponyFiction.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0003_newrating_apply_20150708_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='last_vote_average',
            field=ponyFiction.fields.RatingAverageField(default=3, verbose_name='Последний средний рейтинг'),
        ),
        migrations.AddField(
            model_name='activity',
            name='last_vote_stddev',
            field=models.FloatField(default=0, verbose_name='Последнее среднеквадратичное отклонение'),
        ),
        migrations.AlterField(
            model_name='author',
            name='vk',
            field=models.CharField(max_length=200, verbose_name='VK', blank=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_value',
            field=ponyFiction.fields.RatingField(default=3, verbose_name='Значение'),
        ),
    ]
