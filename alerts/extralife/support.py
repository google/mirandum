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
from extralife.models import *
from django.contrib.auth.models import User

def run_extralife(ffu):
    added = 0
    http = httplib2.Http()
    resp, data = http.request("http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&format=json&participantID=%s" % ffu.profile_id)
    data = json.loads(data)
    events = []
    if len(data):
        for i in data:
            unique_id = i['createdOn']+(i.get('donorName', 'anon') or 'anon')
            if ExtralifeEvent.objects.filter(external_id=unique_id, updater=ffu).count() > 0:
                break
            details = json.dumps(i)
            try:
                ffe = ExtralifeEvent(external_id=unique_id, updater=ffu, details=details)
                ffe.save()
            except Exception, E:
                print "Failed in individual extralife run: %s\nData:\n%s" % (E, details)
            added += 1

    return added

