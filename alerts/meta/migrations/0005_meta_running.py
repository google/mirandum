# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0004_auto_20170521_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='running',
            field=models.BooleanField(default=False),
        ),
    ]
