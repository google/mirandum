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
import json
import iso8601

class FanFundingUpdate(main.models.Updater):
    credentials = models.ForeignKey(AppCreds)

class FanFundingEvent(main.models.UpdaterEvent):
    details = models.TextField()
    updater = models.ForeignKey(FanFundingUpdate)

    def as_dict(self):
        details = json.loads(self.details)
        name = "Anonymous Donor"
        if 'supporterDetails' in details['snippet']:
            name = details['snippet']['supporterDetails']['displayName']
        datetime = iso8601.parse_date(details['snippet']['createdAt'])    
        info = {
            # general 
            'name': name,
            'comment': details['snippet'].get('commentText', ""),
            'donation_amount': float(details['snippet']['amountMicros']) / 1000000.,
            'currency': details['snippet']['currency'],
            
            # Display-friendly
            'amount': details['snippet']['displayString'],
            
            # Filtering friendly
            'amount_micros': int(details['snippet']['amountMicros']),

            'timestamp': datetime,
        }
        return info

class AlertConfig(main.models.AlertConfig):
    blacklist = models.TextField(blank=True, null=True)
    filter_type = models.CharField(max_length=20, choices=(
        ('1equal', 'Equals'),
        ('2gt', 'Greater than'),
        ('3default', 'Default'),
    ), default='3default', help_text="When filtering for specific amounts, comparison to use.")
    filter_amount = models.FloatField(blank=True, null=True)
    text_to_speech = models.BooleanField(default=False)
