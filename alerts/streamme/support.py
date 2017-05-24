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
from streamme.models import *
from django.contrib.auth.models import User

def run_streamme(ffu):
    added = 0
    http = httplib2.Http()
    resp, data = http.request("https://www.stream.me/api-user/v1/%s/followers?limit=5" % ffu.username)
    data = json.loads(data)
    events = []
    if 'reasons' in data:
        raise Exception("Failed to load data for stream.me user %s" % ffu.username)
    if data['_embedded'].get('users'):
        for i in data['_embedded']['users']:
            unique_id = i['userPublicId']
            if StreammeEvent.objects.filter(external_id=unique_id, updater=ffu).count() > 0:
                break
            details = json.dumps(i)
            try:
                ffe = StreammeEvent(external_id=unique_id, updater=ffu, details=details)
                ffe.save()
            except Exception, E:
                print "Failed in individual streamme run: %s\nData:\n%s" % (E, details)
            added += 1

    return added

