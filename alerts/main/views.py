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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import AccessKey, AlertConfig, Alert, Updater, RecentConfig
from main.support import formatter
from main.forms import RecentForm
from main.appconfig import type_data
from donations.models import Donation

@login_required
def home_redirect(request):
    return HttpResponseRedirect("/")

# Create your views here.
@login_required
def home(request):
    key, created = AccessKey.objects.get_or_create(user=request.user)
    if created:
        k = md5.md5(str(random.random())).hexdigest()
        key.key = k
        key.save()
    configs = AlertConfig.objects.filter(user=request.user)
    recents = RecentConfig.objects.filter(user=request.user)
    bad_updaters = Updater.objects.filter(user=request.user, failure_count=5)
    all_updaters = Updater.objects.filter(user=request.user)
    types = set([updater.friendly_type() for updater in all_updaters])
    return render(request, "home.html", {'key': key, 'configs': configs, 'recents': recents, 'bad_updaters': bad_updaters, 'updater_types': sorted(types)})    

@login_required
def alert_page(request):
    key, created = AccessKey.objects.get_or_create(user=request.user)
    if created:
        k = md5.md5(str(random.random())).hexdigest()
        key.key = k
        key.save()
    configs = AlertConfig.objects.filter(user=request.user)
    recents = RecentConfig.objects.filter(user=request.user)
    return render(request, "alert_page.html", {'key': key, 'configs': configs, 'recents': recents})    

@login_required
def reset_key(request):
    if request.POST and 'change' in request.POST:
        key, created = AccessKey.objects.get_or_create(user=request.user)
        k = md5.md5(str(random.random())).hexdigest()
        key.key = k
        key.save()
        return HttpResponseRedirect("/alert_page")
    return render(request, "reset_key.html")

@login_required
def delete_updater(request, id):
    u = Updater.objects.get(pk=id, user=request.user)
    if request.method == 'POST':
        type = u.type
        u.delete()
        if 'redirect' in request.POST:
            return HttpResponseRedirect("/%s/" % u.type)
        else:
            return HttpResponseRedirect("/")
    else:
        return render(request, "delete_update.html")

def alert_popup(request):
    return render(request, "alert_popup.html")

def recent_popup(request):
    return render(request, "recent_popup.html")

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
            'type': alert.config.type,
        })
    output = json.dumps({'alerts': alert_response})
    response = HttpResponse(output)
    response['Access-Control-Allow-Origin'] = "*"
    response['Access-Control-Allow-Headers'] = 'accept, x-requested-with'
    return response

def output_for_recent(config):
    output = []
    if config.type != "donations":
        event = type_data[config.type]['event']
        events = event.objects.filter(updater__user=config.user).order_by("-id")[0:config.count]
        for i in events:
            output.append(formatter(config.format, i.as_dict()))
    else:
        donation = Donation.objects.filter(user=config.user).order_by("-timestamp")[0:config.count]
        for i in donation:
            output.append(formatter(config.format, i.as_dict()))
    return config.seperator.join(output)

def all_recents(request):
    if not 'key' in request.GET: 
        return HttpResponseBadRequest()
    key = request.GET['key']
    k = AccessKey.objects.get(key=key)
    output = {}
    for i in RecentConfig.objects.filter(user=k.user):
        output['%s-%s' % (i.type, i.id)] = output_for_recent(i)
    output_s = json.dumps(output)
    return HttpResponse(output_s, content_type='text/plain')


def recent_api(request):
    if not 'key' in request.GET or not 'id' in request.GET: 
        return HttpResponseBadRequest()
    key = request.GET['key']
    k = AccessKey.objects.get(key=key)
    config = RecentConfig.objects.get(pk=request.GET['id'])
    if config.user != k.user:
        return HttpResponseBadRequest()
    data = output_for_recent(config)
    output = {
      'latest': data,
      'font': config.font or None,
      'font_size': config.font_size or None,
      'font_color': config.font_color or None,
      }
     
    output_s = json.dumps(output)
    return HttpResponse(output_s, content_type='text/plain')

def label_manager(request):
    return render(request, "label_manager.html")

@login_required
def recent_config(request, recent_id=None):
    config = RecentConfig
    form = RecentForm
    ac = None
    if recent_id:
        try:
            ac = config.objects.get(pk=int(recent_id), user=request.user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/lists')
        if request.POST and 'delete' in request.POST:
            ac.delete()
            return HttpResponseRedirect('/lists')
    if request.POST:
        f = form(request.POST, instance=ac)
    else:
        if ac:
            f = form(instance=ac)
        else:
            f = form()
    if f.is_valid():
        ac = f.save(commit=False)
        ac.user = request.user
        ac.save()
        return HttpResponseRedirect("/lists")
        
    return render(request, "recent_config.html", {'form': f, 'new': recent_id is None})

@login_required
def lists(request):
    key, created = AccessKey.objects.get_or_create(user=request.user)
    if created:
        k = md5.md5(str(random.random())).hexdigest()
        key.key = k
        key.save()
    if request.method == "POST" and 'add' in request.POST:
        config = RecentConfig(
            user = request.user,
            count = 1
        )
        if request.POST['add'] == "Add Recent Donation":
            config.type = "donations"
            config.format = "[[name]] ([[currencysymbol]][[amount]]"
            config.save()
        elif request.POST['add'] == "Add Recent Sponsor":
            config.type = "sponsors"
            config.format = "[[name]]"
            config.save()
        elif request.POST['add'] == "Add Recent Subscriber":
            config.type = "ytsubs"
            config.format = "[[name]]"
            config.save()

    recents = RecentConfig.objects.filter(user=request.user)
    return render(request, "lists.html", {'recents': recents, 'key': key})
        

