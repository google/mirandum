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

import django

django.setup()

import json
import httplib2
import time
from datetime import datetime, timedelta
from django.utils import timezone
from fanfunding.models import *
from googaccount.models import CredentialsModel
from django.contrib.auth.models import User

from oauth2client.contrib.django_orm import Storage
BASE_URL = "https://www.googleapis.com/youtube/v3/"
def run_fan_funding(ffu):
    added = 0
    storage = Storage(CredentialsModel, 'id', ffu.credentials, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        return added
    http = httplib2.Http()
    http = credential.authorize(http)
    resp, data = http.request("%sfanFundingEvents?part=snippet&maxResults=5" % BASE_URL)
    data = json.loads(data)
    events = []
    if 'items' in data:
        for i in data['items']:
            if FanFundingEvent.objects.filter(funding_id=i['id'], ffu=ffu).count() > 0:
                break

            details = json.dumps(i)
            try:
                ffe = FanFundingEvent(funding_id=i['id'], ffu=ffu, details=details)
                ffe.save()
            except Exception, E:
                print "Failed in individual fan funding run: %s\nData:\n%s" % (E, details)
            added += 1

    return added

def run():
    while True:
        try:
            time_threshold = datetime.now() - timedelta(seconds=15)
            time_threshold = timezone.make_aware(time_threshold, timezone.get_default_timezone())
            for i in FanFundingUpdate.objects.filter(last_update__lt=time_threshold, failure_count__lt=5):
                try:
                    run_fan_funding(i)
                    i.last_update = timezone.now()
                    i.last_failure = None
                    i.last_failure_message = None
                    i.failure_count = 0
                    i.save()
                except Exception, E:
                    msg = "Attempting to update subs failed for %s: \n   %s: %s" % (i.id, type(E), E)
                    print msg
                    i.last_update = timezone.now()
                    i.last_failure = timezone.now()
                    i.last_failure_message = msg
                    i.failure_count = i.failure_count + 1
                    i.save()
        except Exception, E:
            print "Something very basic went wrong with fan funding."
        time.sleep(1)

if __name__ == "__main__":
    run()
