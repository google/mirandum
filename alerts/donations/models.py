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
from donations.currencymap import SYMBOLS

class Donation(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    primary_amount = models.FloatField(blank=True, null=True)
    primary_currency = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=20)
    def as_dict(self):
        return {
            'name': self.name,
            'comment': self.comment,
            'amount': "%.2f" % self.amount,
            'currency': self.currency,
            'currencysymbol': SYMBOLS.get(self.currency, ""),
        }
