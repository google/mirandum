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
import main.models
import json
from django.utils import timezone
import datetime

class TwitchalertsUpdate(main.models.Updater):
    label = models.CharField(max_length=255, default="")
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    last_id = models.CharField(max_length=255, blank=True, null=True)
    refresh_before = models.DateTimeField()

class TwitchalertsEvent(main.models.UpdaterEvent):
    details = models.TextField()
    updater = models.ForeignKey(TwitchalertsUpdate)

    def as_dict(self):
        details = json.loads(self.details)
        name = "Anonymous"
        if 'name' in details and details['name']:
            name = details['name']
        message = ""
        if 'message' in details and details['message']:
            message = details['message']
        amount = "%.2f" % float(details['amount']) 
        amount = " ".join([amount, details['currency']])
        timestamp = datetime.datetime.utcfromtimestamp(int(details['created_at']))
        timestamp = timezone.make_aware(timestamp, timezone.utc)
        info = {
            'name': name,
            'amount': amount,
            'comment': message,
            'donation_amount': float(details['amount']),
            'currency': details['currency'],
            'timestamp': timestamp,
        }
        return info

class TwitchalertsAlertConfig(main.models.AlertConfig):
    blacklist = models.TextField(blank=True, null=True)
    filter_type = models.CharField(max_length=20, choices=(
        ('1equal', 'Equals'),
        ('2gt', 'Greater than'),
        ('3default', 'Default'),
    ), default='3default', help_text="When filtering for specific amounts, comparison to use.")
    filter_amount = models.FloatField(blank=True, null=True)
