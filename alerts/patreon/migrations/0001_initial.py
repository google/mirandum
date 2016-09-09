# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.contrib.django_orm
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20160802_1524'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatreonAlertConfig',
            fields=[
                ('alertconfig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.AlertConfig')),
                ('blacklist', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('main.alertconfig',),
        ),
        migrations.CreateModel(
            name='PatreonAppCreds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatreonCredentialsModel',
            fields=[
                ('id', models.ForeignKey(primary_key=True, serialize=False, to='patreon.PatreonAppCreds')),
                ('credential', oauth2client.contrib.django_orm.CredentialsField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatreonEvent',
            fields=[
                ('updaterevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.UpdaterEvent')),
                ('details', models.TextField()),
            ],
            options={
            },
            bases=('main.updaterevent',),
        ),
        migrations.CreateModel(
            name='PatreonUpdate',
            fields=[
                ('updater_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.Updater')),
                ('credentials', models.ForeignKey(to='patreon.PatreonAppCreds')),
            ],
            options={
            },
            bases=('main.updater',),
        ),
        migrations.AddField(
            model_name='patreonevent',
            name='updater',
            field=models.ForeignKey(to='patreon.PatreonUpdate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patreonappcreds',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
