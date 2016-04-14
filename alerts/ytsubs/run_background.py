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
from ytsubs.models import *
from googaccount.models import CredentialsModel
from django.contrib.auth.models import User
from apiclient import discovery
from apiclient import errors
from oauth2client.contrib.django_orm import Storage

def ListRecentMessagesMatchingQuery(service, user_id, query=''):
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query, maxResults=10).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def GetMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def run_fan_funding(ffu):
    storage = Storage(CredentialsModel, 'id', ffu.credentials, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        return
    http = httplib2.Http()
    http = credential.authorize(http)
    service = discovery.build('gmail', 'v1', http)
    output = ListRecentMessagesMatchingQuery(service, "me", '"has subscribed to you"')
    added = 0
    for item in output:
        if SubEvent.objects.filter(sub_id=item['id']).count():
            break
        message = GetMessage(service, "me", item['id'])
        headers = message['payload']['headers']
        f, s, d = '', '', ''
        for header in headers:
            if header['name'] == "From": f = header['value']
            if header['name'] == "Subject": s = header['value']
            if header['name'] == "Date": d = header['value']
        if 'noreply@youtube.com' in f:
            s = s.strip().replace(" has subscribed to you on YouTube!", "")
            try:
                e = SubEvent(sub_id=item['id'], details = s, update=ffu)
                e.save()
                added += 1
            except Exception, E:
                print "Failed to create specific subevent for %s: \n    %s: %s" % (ffu.id, type(E), E) 


def run():
    while True:
        time_threshold = datetime.now() - timedelta(seconds=15)
        time_threshold = timezone.make_aware(time_threshold, timezone.get_default_timezone())
        for i in SubUpdate.objects.filter(last_update__lt=time_threshold, failure_count__lt=5):
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

        time.sleep(1)

if __name__ == "__main__":
    run()
