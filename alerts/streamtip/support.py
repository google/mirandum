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
import urllib2
from streamtip.models import *

def run_streamtip(ffu):
    added = 0
    auth = "%s %s" % (ffu.client_id, ffu.access_token)
    request = urllib2.Request("https://streamtip.com/api/tips?limit=10&sort_by=date&&direction=desc", 
        headers={
            "Authorization": auth
            })
    contents = urllib2.urlopen(request).read()
    data = json.loads(contents)
    for i in data['tips']:
        if StreamtipEvent.objects.filter(external_id=i['_id'], updater=ffu).count() > 0:
            break
        details = json.dumps(i)
        try:
            ffe = StreamtipEvent(external_id=i['_id'], updater=ffu, details=details)
            ffe.save()
        except Exception, E:
            print "Failed in individual streamtip run: %s\nData:\n%s" % (E, details)
        added += 1
    return added
