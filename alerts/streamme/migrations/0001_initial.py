# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_recentactivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreammeAlertConfig',
            fields=[
                ('alertconfig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.AlertConfig')),
                ('blacklist', models.TextField(null=True, blank=True)),
            ],
            bases=('main.alertconfig',),
        ),
        migrations.CreateModel(
            name='StreammeEvent',
            fields=[
                ('updaterevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.UpdaterEvent')),
                ('details', models.TextField()),
            ],
            bases=('main.updaterevent',),
        ),
        migrations.CreateModel(
            name='StreammeUpdate',
            fields=[
                ('updater_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.Updater')),
                ('username', models.CharField(max_length=150)),
            ],
            bases=('main.updater',),
        ),
        migrations.AddField(
            model_name='streammeevent',
            name='updater',
            field=models.ForeignKey(to='streamme.StreammeUpdate'),
        ),
    ]
