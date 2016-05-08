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
        ('streamtip', '0002_migrate_updater'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamtipalertconfig',
            name='filter_amount',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamtipalertconfig',
            name='filter_type',
            field=models.CharField(default=b'3default', help_text=b'When filtering for specific amounts, comparison to use.', max_length=20, choices=[(b'1equal', b'Equals'), (b'2gt', b'Greater than'), (b'3default', b'Default')]),
            preserve_default=True,
        ),
    ]
