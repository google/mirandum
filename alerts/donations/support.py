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
from django.utils import timezone
from donations.models import Donation
from django.conf import settings
import json

TARGET_CURRENCY = "USD"

def add_donation(info, user, type):
    timestamp = info.get("timestamp", timezone.now())
    d = Donation(
        user = user,
        name = info['name'],
        comment = info['comment'],
        timestamp = timestamp,
        amount = info['donation_amount'],
        currency = info['currency'],
        type = type
    )
    primary_amount = currency_conversion(info['donation_amount'], info['currency'], TARGET_CURRENCY)
    if primary_amount:
        d.primary_amount = primary_amount
        d.primary_currency = TARGET_CURRENCY
    d.save()
    return d

def currency_conversion(amount, f, t):
    fixerdata = json.load(open(settings.CURRENCY_CONVERSION)) 
    fixerdata['rates']['EUR'] = 1
    rates = fixerdata['rates']
    if not f in rates or not t in rates:
        return None
    return amount * rates[t] / rates[f]
