# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fanfunding', '0005_auto_20160506_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertconfig',
            name='text_to_speech',
            field=models.BooleanField(default=False),
        ),
    ]
