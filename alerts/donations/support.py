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
from main.models import Session
from main.support import formatter
from django.conf import settings
from datetime import timedelta
from django.db.models import Sum, Max
from donations.currencymap import SYMBOLS
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

def output_for_top(top):
    donations = Donation.objects.filter(user=top.user) 
    if top.type == 'session':
        session = Session.objects.filter(user=top.user)
        if session.count():
            session = session[0]
            donations = donations.filter(timestamp__gt=session.session_start)
    elif top.type == "limited" and top.days:
        old_time = timezone.now() - timedelta(days=top.days)
        donations = donations.filter(timestamp__gt=old_time)
    
    donations = donations.values('name').filter(primary_amount__gt=0).annotate(
        donations=Sum('primary_amount'), 
        local_donations=Sum('amount'), 
        local_currency=Max('currency')).order_by("-donations")
    output = []
    for i in donations[0:top.count]:
        symbol = SYMBOLS.get(i['local_currency'], "")
        d = {
            'name': i['name'], 
            'amount': "%.2f" % i['local_donations'], 
            'currency': i['local_currency'], 
            'currencysymbol': symbol
        }
        output.append(formatter(top.format, d)) 
    return top.seperator.join(output)    
