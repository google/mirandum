# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.contrib.django_orm
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_recentactivity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BeamAlertConfig',
            fields=[
                ('alertconfig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.AlertConfig')),
                ('blacklist', models.TextField(null=True, blank=True)),
            ],
            bases=('main.alertconfig',),
        ),
        migrations.CreateModel(
            name='BeamAppCreds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BeamEvent',
            fields=[
                ('updaterevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.UpdaterEvent')),
                ('details', models.TextField()),
            ],
            bases=('main.updaterevent',),
        ),
        migrations.CreateModel(
            name='BeamUpdate',
            fields=[
                ('updater_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.Updater')),
            ],
            bases=('main.updater',),
        ),
        migrations.CreateModel(
            name='BeamCredentialsModel',
            fields=[
                ('id', models.ForeignKey(primary_key=True, serialize=False, to='beam.BeamAppCreds')),
                ('credential', oauth2client.contrib.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='beamupdate',
            name='credentials',
            field=models.ForeignKey(to='beam.BeamAppCreds'),
        ),
        migrations.AddField(
            model_name='beamevent',
            name='updater',
            field=models.ForeignKey(to='beam.BeamUpdate'),
        ),
        migrations.AddField(
            model_name='beamappcreds',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
