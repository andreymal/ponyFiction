# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Название', max_length=128, db_index=True)),
                ('title', models.CharField(verbose_name='Заголовок страницы', max_length=255)),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('updated', models.DateTimeField(verbose_name='Дата обновления', auto_now=True)),
            ],
            options={
                'verbose_name': 'страница',
                'verbose_name_plural': 'страницы',
            },
        ),
    ]
