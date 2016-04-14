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
from googaccount.models import AppCreds
import main.models

class FanFundingUpdate(models.Model):
    credentials = models.ForeignKey(AppCreds)
    last_update = models.DateTimeField()
    last_failure = models.DateTimeField(blank=True,null=True)
    last_failure_message = models.TextField(blank=True, null=True)
    failure_count = models.IntegerField(default=0)

class FanFundingEvent(models.Model):
    funding_id = models.CharField(max_length=255)
    details = models.TextField()
    ffu = models.ForeignKey(FanFundingUpdate)

class AlertConfig(main.models.AlertConfig):
    blacklist = models.TextField(blank=True, null=True)
