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
from beam.models import *
from django.contrib.auth.models import User
from oauth2client.contrib.django_orm import Storage

def load_beam_data(updater):
    label = updater.credentials.label
    userid, _ = label.split("-", 2)
    http = httplib2.Http()
    # TODO(crschmidt): This is not a beam API call.
    resp, data = http.request("https://beam.pro/api/v1/channels/%s/follow?order=followed.createdAt:DESC&fields=username&limit=10&noCount=true" % userid)
    data = json.loads(data)
    if 'error' in data:
        raise Exception("Error fetching beam: %s" % json.dumps(data['error']))
    
    return data

def run_beam(updater, loader=load_beam_data):
    data = loader(updater)
    added = 0
    events = []
    for follower in data:
        unique_id = follower['username']
        if BeamEvent.objects.filter(external_id=unique_id, updater=updater).count() > 0:
            break
        details = json.dumps(follower)
        try:
            ffe = BeamEvent(external_id=unique_id, updater=updater, details=details)
            events.append(ffe)
        except Exception, E:
            print "Failed in individual beam run: %s\nData:\n%s" % (E, details)
    for event in reversed(events):
        try:
            event.save()
            added += 1
        except Exception, E:
            print "Failed in individual beam run: %s\nData:\n%s" % (E, ffe.details)
    return added
