# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ponyFiction', '0008_htmlblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=colorful.fields.RGBColorField(verbose_name='Цвет ссылки', default='#808080'),
        ),
    ]
