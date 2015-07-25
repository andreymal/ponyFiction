# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0007_staticpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='HtmlBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='Название', max_length=128, db_index=True)),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('updated', models.DateTimeField(verbose_name='Дата обновления', auto_now=True)),
            ],
            options={
                'verbose_name': 'html-блок',
                'verbose_name_plural': 'html-блоки',
            },
        ),
    ]
