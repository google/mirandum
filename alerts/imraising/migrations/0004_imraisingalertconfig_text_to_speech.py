# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imraising', '0003_auto_20160507_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='imraisingalertconfig',
            name='text_to_speech',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
