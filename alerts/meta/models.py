#  Copyright 2017 Google Inc. All Rights Reserved.
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
from googaccount.models import AppCreds
from main.support import animations_list, font_effects

class Meta(models.Model):
    appcreds = models.ForeignKey(AppCreds)
    counter = models.IntegerField(default=0)
    type = models.CharField(max_length=50,
        choices=(
            ('youtubesubs', 'YouTube Subscribers'),
            ('youtubeviewers', 'YouTube Concurrents'),
        )
    )
    next_update = models.DateTimeField()
    last_update = models.DateTimeField()
    running = models.BooleanField(default=False)
    pre_text = models.CharField(blank=True, null=True, max_length=255, help_text="e.g 'Sub Goal:'")
    post_text = models.CharField(blank=True, null=True, max_length=255, help_text = "e.g. / 3000")
    font = models.CharField(blank=True, null=True, max_length=255)
    font_size = models.CharField(blank=True, null=True, max_length=255)
    font_color = models.CharField(blank=True, null=True, max_length=255)
    font_effect = models.CharField(blank=True, null=True, max_length=255, choices=font_effects())
    font_weight = models.CharField(blank=True, null=True, max_length=255, default="normal")
    outline_color = models.CharField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(User)
