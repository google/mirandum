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

import json
import urllib,urllib2
from twitchalerts.models import *
from django.utils import timezone
from twitchalerts.app_info import TWITCH_INFO
import datetime

def refresh_twitch(ffu):

    data = {
        'refresh_token': ffu.refresh_token,
        'grant_type': 'refresh_token',
        'client_id': TWITCH_INFO['client_id'],
        'client_secret': TWITCH_INFO['client_secret'],
        'redirect_uri': TWITCH_INFO['redirect_uri']
    }
    request = urllib2.Request("https://www.twitchalerts.com/api/v1.0/token", headers={"Accept" : "application/json", "User-Agent": "Livestream Alerts (python-urllib2)"})
    try:
        u = urllib2.urlopen(request, urllib.urlencode(data))
        data = json.load(u)
    except urllib2.HTTPError, E:
        data = json.load(E)
    if 'error' in data:
        raise Exception("Unable to refresh twitch auth tokens: %s\n%s" % (data['error'], data['message']))
    ffu.access_token = data['access_token']
    ffu.refresh_token = data['refresh_token']
    ffu.refresh_before = timezone.now()+datetime.timedelta(seconds=3000)
    ffu.save()

def run_twitchalerts(ffu):
    added = 0
    now = timezone.now()
    if now > ffu.refresh_before:
        refresh_twitch(ffu)    
    request = urllib2.Request("https://www.twitchalerts.com/api/v1.0/donations?limit=10&access_token=%s" % ffu.access_token, 
        headers={
            "User-Agent": "Livestream Alerts (python-urllib2)",
            })
    contents = urllib2.urlopen(request).read()
    data = json.loads(contents)
    if 'error' in data:
        raise Exception("TwitchAlerts API returned error: %s\n%s" % (data['error'], data['message']))
    for i in data['data']:
        if TwitchalertsEvent.objects.filter(external_id=i['donation_id'], updater=ffu).count() > 0:
            break
        details = json.dumps(i)
        try:
            ffe = TwitchalertsEvent(external_id=i['donation_id'], updater=ffu, details=details)
            ffe.save()
        except Exception, E:
            print "Failed in individual twitchalerts run: %s\nData:\n%s" % (E, details)
        added += 1
    return added
