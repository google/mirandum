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

import sys
import json
import urllib2
from streamjar.models import *
import traceback

def run_streamjar(ffu):
    added = 0
    url = "https://streamjar.tv/api/v1/donations?test=true&apikey=%s" % ffu.access_token
    request = urllib2.Request(url,
        headers={"Accept" : "application/json", "User-Agent": "Livestream Alerts (python-urllib2)"}
    ) 
    resp = urllib2.urlopen(request)
    contents = resp.read()
    data = json.loads(contents)
    for i in data:
        unique_id = i['id']
        if StreamjarEvent.objects.filter(external_id=unique_id, updater=ffu).count() > 0:
            break
        details = json.dumps(i)
        try:
            ffe = StreamjarEvent(external_id=unique_id, updater=ffu, details=details)
            ffe.save()
        except Exception, E:
           exc_type, exc_value, exc_traceback = sys.exc_info()
           traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
           print "Failed in individual streamjar run: %s\nData:\n%s" % (E, details)
        added += 1
    return added
