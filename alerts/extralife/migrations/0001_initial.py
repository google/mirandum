# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20160802_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtralifeAlertConfig',
            fields=[
                ('alertconfig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.AlertConfig')),
                ('blacklist', models.TextField(null=True, blank=True)),
                ('filter_type', models.CharField(default=b'3default', help_text=b'When filtering for specific amounts, comparison to use.', max_length=20, choices=[(b'1equal', b'Equals'), (b'2gt', b'Greater than'), (b'3default', b'Default')])),
                ('filter_amount', models.FloatField(null=True, blank=True)),
                ('text_to_speech', models.BooleanField(default=False)),
            ],
            bases=('main.alertconfig',),
        ),
        migrations.CreateModel(
            name='ExtralifeEvent',
            fields=[
                ('updaterevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.UpdaterEvent')),
                ('details', models.TextField()),
            ],
            bases=('main.updaterevent',),
        ),
        migrations.CreateModel(
            name='ExtralifeUpdate',
            fields=[
                ('updater_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.Updater')),
                ('profile_id', models.IntegerField()),
            ],
            bases=('main.updater',),
        ),
        migrations.AddField(
            model_name='extralifeevent',
            name='updater',
            field=models.ForeignKey(to='extralife.ExtralifeUpdate'),
        ),
    ]
