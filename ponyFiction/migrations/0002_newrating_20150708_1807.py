# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ponyFiction.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='vote_average',
            field=ponyFiction.fields.RatingAverageField(default=3, verbose_name='Средний рейтинг'),
        ),
        migrations.AddField(
            model_name='story',
            name='vote_stddev',
            field=models.FloatField(default=0, verbose_name='Среднеквадратичное отклонение'),
        ),
        migrations.AddField(
            model_name='story',
            name='vote_total',
            field=models.PositiveIntegerField(default=0, verbose_name='Число голосов'),
        ),
        migrations.AddField(
            model_name='vote',
            name='vote_value',
            field=ponyFiction.fields.RatingField(default=3, verbose_name='Значение'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='story',
            field=models.ForeignKey(to='ponyFiction.Story', verbose_name='Оцениваемый рассказ', null=True),
        ),
    ]
