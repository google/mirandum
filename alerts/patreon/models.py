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
from oauth2client.contrib.django_orm import CredentialsField
from django.contrib.auth.models import User
import main.models
import json

class PatreonAppCreds(models.Model):
  user = models.ForeignKey(User, blank=True, null=True)
  label = models.CharField(max_length=255)

class PatreonCredentialsModel(models.Model):
  id = models.ForeignKey(PatreonAppCreds, primary_key=True)
  credential = CredentialsField()

class PatreonUpdate(main.models.Updater):
    credentials = models.ForeignKey(PatreonAppCreds)

class PatreonEvent(main.models.UpdaterEvent):
    details = models.TextField()
    updater = models.ForeignKey(PatreonUpdate)
    
    def as_dict(self):
        details = json.loads(self.details)
        info = {
            'amount': "$%.2f" % (float(details['amount_cents'])/100.),
            'name': details['full_name'],
            'filter_amount': float(details['amount_cents'])/100.,
        }
        return info

class PatreonAlertConfig(main.models.AlertConfig):
    blacklist = models.TextField(blank=True, null=True)
    filter_type = models.CharField(max_length=20, choices=(
        ('1equal', 'Equals'),
        ('2gt', 'Greater than'),
        ('3default', 'Default'),
    ), default='3default', help_text="When filtering for specific amounts, comparison to use.")
    filter_amount = models.FloatField(blank=True, null=True)
