from googaccount.helpers import get_channel
from oauth2client.contrib.django_orm import Storage
from googaccount.models import CredentialsModel
from django.utils import timezone
from datetime import datetime, timedelta
import httplib2, json
BASE_URL = "https://www.googleapis.com/youtube/v3/"

def ytapicall(appcreds, url):
    storage = Storage(CredentialsModel, 'id', appcreds, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        raise Exception("bad creds")
    http = httplib2.Http()
    http = credential.authorize(http)
    resp, data = http.request(url)
    data = json.loads(data)
    if 'error' in data:
        raise Exception("YouTube API Error: %s" % data['error'])
    return data 

def get_subs(appcreds):
    chan = get_channel(appcreds)
    url = "%schannels?part=statistics&id=%s" % (BASE_URL, chan)
    data = ytapicall(appcreds, url)
    sub_count = data['items'][0]['statistics']['subscriberCount']
    return sub_count 
 
f = {
    'subs': get_subs,
}

def update_meta(meta):
    if not meta.type in f:
        raise Exception("Unsupported type")
    count = f[meta.type](meta.appcreds)
    meta.counter = count
    meta.last_update = timezone.now()
    meta.next_update = timezone.now() + timedelta(seconds=60)
    meta.save()
