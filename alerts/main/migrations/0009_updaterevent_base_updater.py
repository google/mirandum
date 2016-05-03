# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_updaterevent_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterevent',
            name='base_updater',
            field=models.ForeignKey(blank=True, to='main.Updater', null=True),
            preserve_default=True,
        ),
    ]
