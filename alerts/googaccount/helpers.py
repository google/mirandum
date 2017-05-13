import httplib2, json
from oauth2client.contrib.django_orm import Storage
from googaccount.models import CredentialsModel
BASE_URL = "https://www.googleapis.com/youtube/v3/"

def get_channel(appcreds, force=False):
    if force == False and appcreds.channel_id:
        return appcreds.channel_id
    storage = Storage(CredentialsModel, 'id', appcreds, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        raise Exception("bad creds")
    http = httplib2.Http()
    http = credential.authorize(http)
    resp, data = http.request("%schannels?part=id&mine=true" % BASE_URL)
    data = json.loads(data)
    if data['pageInfo']['totalResults'] != 1:
        raise Exception("Bad returned channel list: %s" % data)
    channel_id = data['items'][0]['id']
    appcreds.channel_id = channel_id
    appcreds.save()
    return channel_id 
