# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.validators import RegexValidator


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0008_htmlblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(max_length=7, verbose_name='Цвет ссылки', default='#808080', validators=[RegexValidator(regex='^#([0-9A-Fa-f]{3}){1,2}$', message='Это не похоже на цвет')]),
        ),
    ]
