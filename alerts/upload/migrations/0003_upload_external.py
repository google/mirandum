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

def migrate_urls(apps, schema_editor):
    ac = apps.get_model("main", "AlertConfig")
    Upload = apps.get_model("upload", "Upload")
    for u in Upload.objects.filter(type=None):
        u.type = 'unknown'
        u.save()
    for config in ac.objects.all():
        if config.image_url:
            u, created = Upload.objects.get_or_create(user=config.user, remote_path=config.image_url)
            if created:
                u.external = True
                u.local_name = config.image_url
                u.type = 'image'
            u.save()
        if config.sound_url:
            u, created = Upload.objects.get_or_create(user=config.user, remote_path=config.sound_url)
            if created:
                u.external = True
                u.local_name = config.sound_url
                u.type = 'sound'
            u.save()
        
        



class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20160617_1016'),
        ('upload', '0002_auto_20160501_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='external',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RunPython(migrate_urls)
    ]
