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

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from main.models import AccessKey
from main.support import formatter, check_google_font, update_last_activity
from actions.models import Action
from actions.utils import send_yt_chat_message
from django.contrib.auth.decorators import login_required

# Create your views here.

def send_youtube_message(action, params=None):
    message = action.data
    user = action.user
    videos = send_yt_chat_message(user, message)
    return "Message sent to videos: %s" % (",".join(videos))


action_mapping = {
    'send_youtube_message': send_youtube_message
}

def go(request):
    key = request.GET['key']
    k = AccessKey.objects.get(key=key)
    update_last_activity(k.user)
    action = Action.objects.get(pk=request.GET['id'])
    params = {}
    for param in request.GET:
        if param in ['key', 'id']: continue
        params[param] = request.GET['param']
    if action.action_type in action_mapping:
        data = action_mapping[action.action_type](action, params)
    else:
        data = ""
    return HttpResponse(data)

@login_required
def setup(request, action_type=None):
    if action_type and action_type not in action_mapping.keys():
        raise Exception("Unknown action type: %s" % action_type)
    if request.method == "POST" and 'action' in request.POST:
        if request.POST['action'] == "delete":
            a = Action.objects.get(user=request.user, id=request.POST['id'])
            a.delete()
            return HttpResponseRedirect("/actions/")
    if request.method == "POST" and not action_type:
        raise Exception("POST requires action_type (got %s)" % action_type)
    if request.method == "POST":
        a = Action(
            user=request.user,
            action_type=action_type,
            data = request.POST['data']
        )
        a.save()
        return HttpResponseRedirect("/actions/")
    if action_type:
        return render(request, "actions/%s.html" % action_type)
    
    k = AccessKey.objects.get(user=request.user)
    actions = Action.objects.filter(user=request.user)
    return render(request, "actions/list.html", {'actions': actions, 'key': k.key})
