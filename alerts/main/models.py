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
from main.support import animations_list, font_effects

class LastActivity(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()

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
    image_url = models.TextField(blank=True,null=True,
        help_text='<a href="/upload/upload">Upload new file</a>')
    sound_url = models.TextField(blank=True,null=True,
        help_text='<a href="/upload/upload">Upload new files</a>. Note: You need to use a .wav file in most broadcasting software.')
    alert_text = models.TextField(blank=True,null=True)
    font = models.CharField(blank=True, null=True, max_length=255)
    font_size = models.CharField(blank=True, null=True, max_length=255, help_text="Use CSS font sizes, e.g. '64px'", default="64px")
    font_color = models.CharField(blank=True, null=True, max_length=255)
    layout = models.CharField(blank=True, null=True, max_length=100, choices=(
        ('vertical', "Image above text"),
        ('side', 'Image next to text'),
        ('above', 'Text on top of image'),
    ), help_text="Alert layout (only available with v2 AlertBox)")
    animation_in = models.CharField(blank=True, null=True, max_length=100, choices=animations_list("in"), default="fadeIn", help_text="(only available with v2 AlertBox)")
    animation_out = models.CharField(blank=True, null=True, max_length=100, choices=animations_list("out"), default="fadeOut", help_text="(only available with v2 AlertBox)")
    font_effect = models.CharField(blank=True, null=True, max_length=100, choices=font_effects(), default="shadow", help_text="(only available with v2 AlertBox)")
    user = models.ForeignKey(User)
    type = models.CharField(max_length=255)
    def friendly_type(self):
        from main.appconfig import type_data
        appdata = type_data.get(self.type, None)
        if not appdata: return self.type
        return appdata.get('label', self.type)

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
    running = models.BooleanField(default=False)
    type = models.CharField(max_length=255)
    def friendly_type(self):
        from main.appconfig import type_data
        appdata = type_data.get(self.type, None)
        if not appdata: return self.type
        return appdata.get('label', self.type)

    def __str__(self):
        return 'Updater{type=%s}' % self.type


class UpdaterEvent(models.Model):
    external_id = models.CharField(max_length=255, db_index=True)
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
    font_effect = models.CharField(blank=True, null=True, max_length=255, default=None, choices=font_effects())
    font_weight = models.CharField(blank=True, null=True, max_length=255, default="normal")
    outline_color = models.CharField(blank=True, null=True, max_length=255, default=None)

class Session(models.Model):
    user = models.ForeignKey(User)
    session_start = models.DateTimeField()
