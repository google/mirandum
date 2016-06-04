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
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=1)),
                ('format', models.CharField(default=b'[[name]]: [[currencysymbol]][[amount]]', max_length=1000)),
                ('seperator', models.CharField(default=b', ', max_length=100)),
                ('font', models.CharField(max_length=255, null=True, blank=True)),
                ('font_size', models.CharField(max_length=255, null=True, blank=True)),
                ('font_color', models.CharField(max_length=255, null=True, blank=True)),
                ('days', models.IntegerField(null=True, blank=True)),
                ('type', models.CharField(default=b'session', max_length=50, choices=[(b'session', b'Session'), (b'limited', b'Number of Days'), (b'alltime', b'All Time')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
