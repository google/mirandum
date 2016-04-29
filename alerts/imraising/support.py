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
from imraising.models import *

def run_imraising(ffu):
    added = 0
    k = ffu.api_key
    request = urllib2.Request("https://imraising.tv/api/v1/donations?limit=10", 
        headers={
            "Content-Type" : "application/json",
            "Authorization": 'APIKey apikey="%s"' % k
            })
    contents = urllib2.urlopen(request).read()
    data = json.loads(contents)
    for i in data:
        if ImraisingEvent.objects.filter(external_id=i['_id'], updater=ffu).count() > 0:
            break
        details = json.dumps(i)
        try:
            ffe = ImraisingEvent(external_id=i['_id'], updater=ffu, details=details)
            ffe.save()
        except Exception, E:
            print "Failed in individual imraising run: %s\nData:\n%s" % (E, details)
        added += 1
    return added
