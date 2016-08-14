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
import httplib2
from twitchfollows.models import *
from twitchaccount.models import TwitchCredentialsModel
from django.contrib.auth.models import User

from oauth2client.contrib.django_orm import Storage

def run_twitchfollows(ffu):
    added = 0
    http = httplib2.Http()
    #FIXME
    resp, data = http.request("https://api.twitch.tv/kraken/channels/%s/follows" % ffu.credentials.label)
    data = json.loads(data)
    if 'error' in data:
        raise Exception("Error fetching twitchsubs: %s" % json.dumps(data['error']))
    events = []
    if 'follows' in data:
        for i in data['follows']:
            #FIXME
            unique_id = i['user']['name']
            if TwitchFollowEvent.objects.filter(external_id=unique_id, updater=ffu).count() > 0:
                break

            details = json.dumps(i)
            try:
                ffe = TwitchFollowEvent(external_id=unique_id, updater=ffu, details=details)
                events.append(ffe)
            except Exception, E:
                print "Failed in individual twitchsubs run: %s\nData:\n%s" % (E, details)
            added += 1
        for event in reversed(events):
            try:
                event.save()
                added += 1
            except Exception, E:
                print "Failed in individual sponsor run: %s\nData:\n%s" % (E, ffe.details)

    return added
