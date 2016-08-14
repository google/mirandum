# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20160802_1524'),
        ('twitchaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitchFollowAlertConfig',
            fields=[
                ('alertconfig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.AlertConfig')),
                ('blacklist', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('main.alertconfig',),
        ),
        migrations.CreateModel(
            name='TwitchFollowEvent',
            fields=[
                ('updaterevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.UpdaterEvent')),
                ('details', models.TextField()),
            ],
            options={
            },
            bases=('main.updaterevent',),
        ),
        migrations.CreateModel(
            name='TwitchFollowUpdate',
            fields=[
                ('updater_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.Updater')),
                ('credentials', models.ForeignKey(to='twitchaccount.TwitchAppCreds')),
            ],
            options={
            },
            bases=('main.updater',),
        ),
        migrations.AddField(
            model_name='twitchfollowevent',
            name='updater',
            field=models.ForeignKey(to='twitchfollows.TwitchFollowUpdate'),
            preserve_default=True,
        ),
    ]
