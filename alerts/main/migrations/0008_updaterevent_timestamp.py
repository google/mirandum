# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_updater_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterevent',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 12, 34, 24, 588226, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
