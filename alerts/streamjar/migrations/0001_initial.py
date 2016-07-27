# -*- coding: utf-8 -*-
#  Copyright 2016 Google Inc. All Rights Reserved.
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License. 
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20160727_0236'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamjarAlertConfig',
            fields=[
                ('alertconfig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.AlertConfig')),
                ('blacklist', models.TextField(null=True, blank=True)),
                ('filter_type', models.CharField(default=b'3default', help_text=b'When filtering for specific amounts, comparison to use.', max_length=20, choices=[(b'1equal', b'Equals'), (b'2gt', b'Greater than'), (b'3default', b'Default')])),
                ('filter_amount', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=('main.alertconfig',),
        ),
        migrations.CreateModel(
            name='StreamjarEvent',
            fields=[
                ('updaterevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.UpdaterEvent')),
                ('details', models.TextField()),
            ],
            options={
            },
            bases=('main.updaterevent',),
        ),
        migrations.CreateModel(
            name='StreamjarUpdate',
            fields=[
                ('updater_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.Updater')),
                ('access_token', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=('main.updater',),
        ),
        migrations.AddField(
            model_name='streamjarevent',
            name='updater',
            field=models.ForeignKey(to='streamjar.StreamjarUpdate'),
            preserve_default=True,
        ),
    ]
