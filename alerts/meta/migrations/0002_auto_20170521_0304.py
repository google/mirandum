# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meta',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'youtubesubs', b'YouTube Subscribers')]),
        ),
    ]
