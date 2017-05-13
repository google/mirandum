# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('googaccount', '0002_appcreds_channel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=50)),
                ('next_update', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
                ('appcreds', models.ForeignKey(to='googaccount.AppCreds')),
            ],
        ),
    ]
