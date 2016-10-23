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
from patreon.models import *
from django.contrib.auth.models import User
from oauth2client.contrib.django_orm import Storage

def load_patreon_data(updater):
    storage = Storage(PatreonCredentialsModel, 'id', updater.credentials, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        raise Exception("bad creds")
    http = httplib2.Http()
    http = credential.authorize(http)
    resp, data = http.request("https://api.patreon.com/oauth2/api/current_user/campaigns?include=pledges")
    data = json.loads(data)
    if 'error' in data:
        raise Exception("Error fetching patreon: %s" % json.dumps(data['error']))
    data_map = {}
    for i in data['included']:
        data_map['%s-%s' % (i['id'], i['type'])]  = i
    pledges = []
    for campaign in data['data']:
        for i in campaign['relationships']['pledges']['data']:
            pledge_id = i['id']
            pledge_obj = data_map['%s-pledge' % pledge_id]
            patron_id = pledge_obj['relationships']['patron']['data']['id']
            user_obj = data_map['%s-user' % patron_id]
            pledge = user_obj['attributes']
            pledge.update(pledge_obj['attributes'])
            pledge['id'] = pledge_id
            pledges.append(pledge)
    pledges = sorted(pledges, key=lambda x: x['created_at'], reverse=True)
    return pledges

def run_patreon(updater, loader=load_patreon_data):
    data = loader(updater)
    added = 0
    events = []
    for pledge in data:
        unique_id = pledge['id']
        if PatreonEvent.objects.filter(external_id=unique_id, updater=updater).count() > 0:
            break
        details = json.dumps(pledge)
        try:
            ffe = PatreonEvent(external_id=unique_id, updater=updater, details=details)
            events.append(ffe)
        except Exception, E:
            print "Failed in individual patreon run: %s\nData:\n%s" % (E, details)
    for event in reversed(events):
        try:
            event.save()
            added += 1
        except Exception, E:
            print "Failed in individual patreon run: %s\nData:\n%s" % (E, ffe.details)
    return added
