from googaccount.helpers import get_channel
from oauth2client.contrib.django_orm import Storage
from googaccount.models import CredentialsModel
from django.utils import timezone
from datetime import datetime, timedelta
import httplib2, json
from meta.models import Meta
import time
import threading
from main.models import LastActivity

import django

django.setup()

DEFAULT_UPDATE_INTERVAL = 30

BASE_URL = "https://www.googleapis.com/youtube/v3/"

DEBUG = True

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

def get_youtube_subs(appcreds):
    chan = get_channel(appcreds)
    url = "%schannels?part=statistics&id=%s" % (BASE_URL, chan)
    data = ytapicall(appcreds, url)
    sub_count = data['items'][0]['statistics']['subscriberCount']
    return sub_count 

def get_viewers_for_vid(appcreds, vid):
    url = "%svideos?part=liveStreamingDetails&id=%s" % (BASE_URL, chan)
    data = ytapicall(appcreds, url)
    viewers = 0
    if 'items' in data and len(data['items']):
        viewers = int(data['items'][0]['liveStreamingDetails']['concurrentViewers'])
    return viewers
def get_likes_for_vid(appcreds, vid):
    url = "%svideos?part=statistics&id=%s" % (BASE_URL, chan)
    data = ytapicall(appcreds, url)
    likes = 0 
    if 'items' in data and len(data['items']):
        likes = int(data['items'][0]['statistics']['likeCount'])
    return likes
    

def get_youtube_viewers(appcreds):
    url = "%sliveBroadcasts?broadcastType=all&part=snippet&broadcastStatus=active&maxResults=50&" % (BASE_URL)
    data = ytapicall(appcreds, url)
    m = 0
    for event in data['items']:
        viewers = get_viewers_for_vid(appcreds, event['id'])
        if viewers > m:
            m = viewers
    return m
def get_youtube_likes(appcreds):
    url = "%sliveBroadcasts?broadcastType=all&part=snippet&broadcastStatus=active&maxResults=50&" % (BASE_URL)
    data = ytapicall(appcreds, url)
    m = 0
    for event in data['items']:
        likes = get_likes_for_vid(appcreds, event['id'])
        if likes > m:
            m = likes
    return m

f = {
    'youtubesubs': get_youtube_subs,
    'youtubeviewers': get_youtube_viewers,
    'youtubelikes': get_youtube_likes,
}

def update_meta(meta, delay=DEFAULT_UPDATE_INTERVAL):
    if not meta.type in f:
        raise Exception("Unsupported type")
    count = f[meta.type](meta.appcreds)
    meta.counter = count
    meta.last_update = timezone.now()
    meta.next_update = timezone.now() + timedelta(seconds=delay)
    meta.save()

def thread_runner(instance):
    if DEBUG:
        print "running instance", instance.id
    runtime = time.time()
    delay = DEFAULT_UPDATE_INTERVAL
    try:
        lu = LastActivity.objects.filter(user=instance.user)
        recent = timezone.now() - timedelta(seconds=120)
        if not lu.count() or lu[0].timestamp < recent:
            if DEBUG: print "Not active"
            delay = delay * 20
        else:
            if DEBUG: print "Active"
        update_meta(instance, delay)
        instance.running = False
        instance.save()
    except KeyboardInterrupt, E:
        msg = "Attempting to update %s failed for %s: \n   %s: %s" % (instance.type, instance.id, type(E), E)
        print msg
        # we don't update last_update on failure.
        instance.next_update = timezone.now() + timedelta(seconds=delay)
        instance.running = False
        instance.save()
    if DEBUG:
        print "finished", instance.id, " in ", time.time()-runtime

def run():
    # Reset any running tasks at runner start; if anything got stuck
    # because of a restart, we want to clear it when we start.
    for i in Meta.objects.filter(running=True):
        i.running = False
        i.save()
    while True:
        try:
            time_threshold = timezone.now()
            for i in Meta.objects.filter(next_update__lt=time_threshold, running=False).order_by('next_update'):
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
