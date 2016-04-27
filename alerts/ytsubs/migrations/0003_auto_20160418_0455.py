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
        ('main', '0006_updater_updaterevent'),
        ('ytsubs', '0002_auto_20160414_0317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subevent',
            name='id',
        ),
        migrations.RemoveField(
            model_name='subevent',
            name='sub_id',
        ),
        migrations.RemoveField(
            model_name='subupdate',
            name='failure_count',
        ),
        migrations.RemoveField(
            model_name='subupdate',
            name='id',
        ),
        migrations.RemoveField(
            model_name='subupdate',
            name='last_failure',
        ),
        migrations.RemoveField(
            model_name='subupdate',
            name='last_failure_message',
        ),
        migrations.RemoveField(
            model_name='subupdate',
            name='last_update',
        ),
        migrations.AddField(
            model_name='subevent',
            name='updaterevent_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=2, serialize=False, to='main.UpdaterEvent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subupdate',
            name='updater_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=2, serialize=False, to='main.Updater'),
            preserve_default=False,
        ),
    ]
