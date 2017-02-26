# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitchalerts', '0004_auto_20160508_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitchalertsupdate',
            name='label',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
