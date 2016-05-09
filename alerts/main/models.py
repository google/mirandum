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

from django.db import models
from django.contrib.auth.models import User
import md5, random, datetime


class AlertStyle(models.Model):
    image = models.TextField(blank=True,null=True)
    sound = models.TextField(blank=True,null=True)
    font = models.CharField(blank=True, null=True, max_length=255)
    font_size = models.CharField(blank=True, null=True, max_length=255)
    font_color = models.CharField(blank=True, null=True, max_length=255)
    position = models.CharField(max_length=20, choices = (
        ('center', 'Centered'),
        ('top', 'Top'),
        ), default='center')

class AlertConfig(models.Model):
    image_url = models.TextField(blank=True,null=True)
    sound_url = models.TextField(blank=True,null=True)
    alert_text = models.TextField(blank=True,null=True)
    font = models.CharField(blank=True, null=True, max_length=255)
    font_size = models.CharField(blank=True, null=True, max_length=255)
    font_color = models.CharField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=255)

class Alert(models.Model):
    text = models.TextField()
    time = models.DateTimeField()
    delivered = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    style = models.ForeignKey(AlertStyle)
    config = models.ForeignKey(AlertConfig, blank=True, null=True)
    test = models.BooleanField(default=False)

class AccessKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=200)

class Updater(models.Model):
    last_update = models.DateTimeField(default=datetime.datetime(1990,1,1,0,0,0))
    next_update = models.DateTimeField(default=datetime.datetime(1990,1,1,0,0,0))
    last_failure = models.DateTimeField(blank=True,null=True)
    last_failure_message = models.TextField(blank=True, null=True)
    failure_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True)
    type = models.CharField(max_length=255)

class UpdaterEvent(models.Model):
    external_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    base_updater = models.ForeignKey(Updater, blank=True, null=True)

class RecentConfig(models.Model):
    user = models.ForeignKey(User)
    count = models.IntegerField(default=3)
    format = models.CharField(default='[[name]]', max_length=1000)
    seperator = models.CharField(default=', ', max_length=100)
    type = models.CharField(max_length=50)
    font = models.CharField(blank=True, null=True, max_length=255)
    font_size = models.CharField(blank=True, null=True, max_length=255)
    font_color = models.CharField(blank=True, null=True, max_length=255)
