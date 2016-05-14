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
from sponsors.models import *
from googaccount.models import CredentialsModel
from django.contrib.auth.models import User
from oauth2client.contrib.django_orm import Storage
BASE_URL = "https://www.googleapis.com/youtube/v3/"

def load_sponsor_data(updater):
    storage = Storage(CredentialsModel, 'id', updater.credentials, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        raise Exception("bad creds")
    http = httplib2.Http()
    http = credential.authorize(http)
    resp, data = http.request("%ssponsors?part=snippet&maxResults=5&filter=all" % BASE_URL)
    data = json.loads(data)
    if 'error' in data:
        raise Exception("Error fetching sponsors: %s" % json.dumps(data['error']))
    return data

def run_sponsors(updater, loader=load_sponsor_data):
    data = loader(updater)
    added = 0
    events = []
    if 'items' in data:
        for i in data['items']:
            snippet = i['snippet']
            unique_id = "%s-%s" % (snippet.get('channelId', "unknown-channel"), snippet.get('sponsorSince', 'unknown'))
            if SponsorEvent.objects.filter(external_id=unique_id, updater=updater).count() > 0:
                break
            details = json.dumps(i)
            try:
                ffe = SponsorEvent(external_id=unique_id, updater=updater, details=details)
                events.append(ffe)
            except Exception, E:
                print "Failed in individual sponsor run: %s\nData:\n%s" % (E, details)
        for event in reversed(events):
            try:
                event.save()
                added += 1
            except Exception, E:
                print "Failed in individual sponsor run: %s\nData:\n%s" % (E, ffe.details)
    return added
