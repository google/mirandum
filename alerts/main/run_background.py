#!/usr/bin/python

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

import time
from datetime import datetime, timedelta
from django.utils import timezone
from main.models import Updater

from fanfunding.support import run_fan_funding
from ytsubs.support import run_subs
from sponsors.support import run_sponsors
from streamtip.support import run_streamtip
from twitchalerts.support import run_twitchalerts
from imraising.support import run_imraising

META = {
    'fanfunding': {
        'runner': run_fan_funding,
        'prop': 'fanfundingupdate'
    },
    'ytsubs': {
        'runner': run_subs,
        'prop': 'subupdate'
    },
    'sponsors': {
        'runner': run_sponsors,
        'prop': 'sponsorupdate'
    },
    'streamtip': {
        'runner': run_streamtip,
        'prop': 'streamtipupdate'
    },
    'twitchalerts': {
        'runner': run_twitchalerts,
        'prop': 'twitchalertsupdate'
    },
    'imraising': {
        'runner': run_imraising,
        'prop': 'imraisingupdate'
    }
        
}

def run():
    while True:
        try:
            time_threshold = datetime.now() - timedelta(seconds=15)
            time_threshold = timezone.make_aware(time_threshold, timezone.get_default_timezone())
            for i in Updater.objects.filter(last_update__lt=time_threshold, failure_count__lt=5):
                updater_props = META.get(i.type, None)
                if not updater_props: continue
                
                runner = updater_props['runner']

                i = getattr(i, updater_props['prop'])
                try:
                    runner(i)
                    i.last_update = timezone.now()
                    i.last_failure = None
                    i.last_failure_message = None
                    i.failure_count = 0
                    i.save()
                except Exception, E:
                    msg = "Attempting to update %s failed for %s: \n   %s: %s" % (i.type, i.id, type(E), E)
                    print msg
                    i.last_update = timezone.now()
                    i.last_failure = timezone.now()
                    i.last_failure_message = msg
                    i.failure_count = i.failure_count + 1
                    i.save()
        except Exception, E:
            print "Something very basic went wrong with something: %s" % E
        time.sleep(1)

if __name__ == "__main__":
    run()
