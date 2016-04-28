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

import md5
import json
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import AccessKey, AlertConfig, Alert

# Create your views here.
@login_required
def home(request):
    return HttpResponseRedirect("/alert_page")

@login_required
def alert_page(request):
    key, created = AccessKey.objects.get_or_create(user=request.user)
    if created:
        k = md5.md5(str(random.random())).hexdigest()
        key.key = k
        key.save()
    configs = AlertConfig.objects.filter(user=request.user)
    return render(request, "alert_page.html", {'key': key, 'configs': configs})    

@login_required
def reset_key(request):
    if request.POST and 'change' in request.POST:
        key, created = AccessKey.objects.get_or_create(user=request.user)
        k = md5.md5(str(random.random())).hexdigest()
        key.key = k
        key.save()
        return HttpResponseRedirect("/alert_page")
    return render(request, "reset_key.html")

def alert_popup(request):
    return render(request, "alert_popup.html")

def alert_api(request):
    key = request.GET['key']
    k = AccessKey.objects.get(key=key)
    alerts = Alert.objects.filter(user=k.user).order_by("-id")
    alert_response = []
    for alert in alerts[0:10]:
        alert_response.append({
            'id': alert.id,
            'text': alert.text,
            'image': alert.style.image,
            'sound': alert.style.sound,
            'font': alert.style.font,
            'font_size': alert.style.font_size,
            'font_color': alert.style.font_color,
        })
    output = json.dumps({'alerts': alert_response})
    response = HttpResponse(output)
    response['Access-Control-Allow-Origin'] = "*"
    response['Access-Control-Allow-Headers'] = 'accept, x-requested-with'
    return response
