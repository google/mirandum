# -*- coding: utf-8 -*-
#  Copyright 2017 Google Inc. All Rights Reserved.
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


from googaccount.helpers import get_channel
from oauth2client.contrib.django_orm import Storage
from googaccount.models import CredentialsModel, AppCreds
from django.utils import timezone
from datetime import datetime, timedelta
import httplib2, json
BASE_URL = "https://www.googleapis.com/youtube/v3/"

class YouTubeAPIException(Exception):
    pass
class CredentialsException(Exception):
    pass

def ytapicall(appcreds, url, post_json=None):
    storage = Storage(CredentialsModel, 'id', appcreds, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        raise CredentialsException("bad creds")
    http = httplib2.Http()
    http = credential.authorize(http)
    if post_json:
        resp, data = http.request(url, "POST", json.dumps(post_json), headers = {'content-type': 'application/json'})
    else:
        resp, data = http.request(url)
    data = json.loads(data)
    if 'error' in data:
        e = YouTubeAPIException("YouTube API Error: %s" % data['error']['message'])
        e.data = data
        raise e
    return data 

def send_yt_chat_message(user, message):
    live_chat_ids = []
    video_ids = []
    for appcreds in AppCreds.objects.filter(user=user):
        for event_type in ('upcoming', 'active'):
            url = "%sliveBroadcasts?broadcastType=all&part=snippet&broadcastStatus=%s&maxResults=50" % (BASE_URL, event_type)
            try:
                data = ytapicall(appcreds, url)
                print data
                for i in data['items']:
                    if 'snippet' in i and 'liveChatId' in i['snippet']:
                        live_chat_id = i['snippet']['liveChatId']
                        live_chat_ids.append((live_chat_id, appcreds))
                        video_ids.append(i['id'])
            except YouTubeAPIException, E:
                print E
                continue
            except CredentialsException, E:
                print E
                continue
    live_chat_ids = set(live_chat_ids)
    for live_chat_id in live_chat_ids:
        data = {'snippet': {'type': 'textMessageEvent', 'liveChatId': live_chat_id[0], 'textMessageDetails': {'messageText': message}}} 
        url = "%sliveChat/messages?part=snippet" % BASE_URL
        print ytapicall(live_chat_id[1], url, post_json=data)
    return video_ids

if __name__ == "__main__":
    import django

    django.setup()
    from django.contrib.auth.models import User
    u = User.objects.get(pk=6)
    send_yt_chat_message(u, "foo 💩 :awesome:")
