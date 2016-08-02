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

import math
import threading
import time
from datetime import datetime, timedelta
from django.utils import timezone
from main.models import Updater, LastActivity
from main.appconfig import type_data


from django.conf import settings

DEBUG = settings.RUNNER_DEBUG

DEFAULT_UPDATE_INTERVAL = 15

def thread_runner(instance):
    if DEBUG:
        print "running instance", instance.id
    runtime = time.time()
    delay = DEFAULT_UPDATE_INTERVAL
    try:
        updater_props = type_data.get(instance.type, None)
        delay = updater_props.get('delay', DEFAULT_UPDATE_INTERVAL)
        lu = LastActivity.objects.filter(user=instance.user)
        recent = timezone.now() - timedelta(seconds=120)
        if not lu.count() or lu[0].timestamp < recent:
            if DEBUG: print "Not active"
            delay = delay * 8
        else:
            if DEBUG: print "Active"
        runner = updater_props['runner']
        instance = getattr(instance, updater_props['prop'])
        runner(instance)
        instance.last_update = timezone.now()
        instance.next_update = timezone.now() + timedelta(seconds=delay)
        # We leave messages + timestamps so we can see old failures even if the system recovered.
        instance.failure_count = 0
        instance.running = False
        instance.save()
    except Exception, E:
        msg = "Attempting to update %s failed for %s: \n   %s: %s" % (instance.type, instance.id, type(E), E)
        print msg
        # we don't update last_update on failure.
        instance.last_failure = timezone.now()
        instance.last_failure_message = msg
        instance.failure_count = instance.failure_count + 1
        # exponential backoff
        update_time = delay * math.pow(3, instance.failure_count)
        instance.next_update = timezone.now() + timedelta(seconds=update_time)
        instance.running = False
        instance.save()
    if DEBUG:
        print "finished", instance.id, " in ", time.time()-runtime

def run():
    # Reset any running tasks at runner start; if anything got stuck
    # because of a restart, we want to clear it when we start.
    for i in Updater.objects.filter(running=True):
        i.running = False
        i.save()
    while True:
        try:
            time_threshold = timezone.now()
            for i in Updater.objects.filter(next_update__lt=time_threshold, failure_count__lt=5, running=False).order_by('next_update'):
                updater_props = type_data.get(i.type, None)
                if not updater_props: continue
                
                i = getattr(i, updater_props['prop'])
                # Set next update here; then reset it again when the function actually finishes.
                i.running = True
                i.save()
                t = threading.Thread(target=thread_runner, args=[i])
                t.start()

        except Exception, E:
            print "Something very basic went wrong with something: %s" % E
        time.sleep(1)

if __name__ == "__main__":
    run()
