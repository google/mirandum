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
        short_amount = "%.2f" % self.amount
        if round(self.amount, 0) == self.amount:
            short_amount = "%.0f" % self.amount
        return {
            'name': self.name,
            'comment': self.comment,
            'amount': "%.2f" % self.amount,
            'amount_integer': "%.0f" % self.amount,
            'amount_short': short_amount,
            'currency': self.currency,
            'currencysymbol': SYMBOLS.get(self.currency, ""),
        }

class TopList(models.Model):
    user = models.ForeignKey(User)
    count = models.IntegerField(default=1)
    format = models.CharField(default='[[name]]: [[currencysymbol]][[amount]]', max_length=1000)
    seperator = models.CharField(default=', ', max_length=100)
    font = models.CharField(blank=True, null=True, max_length=255)
    font_size = models.CharField(blank=True, null=True, max_length=255)
    font_color = models.CharField(blank=True, null=True, max_length=255)
    days = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=(
        ('session', 'Session'),
        ('limited', 'Number of Days'),
        ('alltime', 'All Time'),
    ), default='session')

class Goal(models.Model):
    user = models.ForeignKey(User)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    source_type = models.CharField(max_length=100, help_text="Limit donations to a specific type of donation for this goal.", default='', choices=(
        ('', 'All types'),
        ('extralife', 'Extra Life'),
        ('fanfunding', 'Fan Funding'),
        ('imraising', 'Imraising'),
        ('twitchalerts', 'Twitch Alerts/Stream Labs'),
        ('streamjar', 'Stream Jar'),
        ('streamtip', 'Stream Tip')))
