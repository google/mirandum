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

import datetime
import urllib, urllib2
import json

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import django.forms as forms

from main.support import ac
from twitchalerts.models import TwitchalertsUpdate, TwitchalertsAlertConfig 
from twitchalerts.signals import config_to_alert
from twitchalerts.app_info import TWITCH_INFO

MODULE_NAME = "twitchalerts"

@login_required
def home(request):
    ffconfigs = TwitchalertsUpdate.objects.filter(user=request.user)
    alerts = TwitchalertsAlertConfig.objects.filter(user=request.user)
    return render(request, "twitchalerts/home.html", {'configs': ffconfigs,
        'alerts': alerts})

class TwitchalertsForm(forms.Form):
    client_id = forms.CharField()
    access_token = forms.CharField()

@login_required
def setup(request):
    if 'code' not in request.GET:
        url_data = {
            'client_id': TWITCH_INFO['client_id'],
            'redirect_uri': TWITCH_INFO['redirect_uri'],
            'response_type': 'code',
            'scope': 'donations.read'
        }
        return HttpResponseRedirect("https://www.twitchalerts.com/api/v1.0/authorize?%s" % urllib.urlencode(url_data))
    data = {
        'code': request.GET['code'],
        'grant_type': 'authorization_code',
        'client_id': TWITCH_INFO['client_id'],
        'client_secret': TWITCH_INFO['client_secret'],
        'redirect_uri': TWITCH_INFO['redirect_uri']
    }
    twitch_request = urllib2.Request("https://www.twitchalerts.com/api/v1.0/token", headers= {
    'Accept': 'application/json',
    'User-Agent': 'Livestream Alerts (python-urllib2)'
    })
    try:
        u = urllib2.urlopen(twitch_request, urllib.urlencode(data))
        data = json.load(u)
    except urllib2.HTTPError, E:
        data = json.load(E)
        raise Exception("TwitchAlerts API Failure: %s: %s" % (data['error'], data['message']))
    refresh_before = timezone.now() + datetime.timedelta(seconds=3000)
    tau = TwitchalertsUpdate(
        access_token = data['access_token'],
        refresh_token = data['refresh_token'],
        user=request.user,
        type="twitchalerts",
        refresh_before=refresh_before,
    )
    tau.save()
    return HttpResponseRedirect("/twitchalerts/")

class AlertForm(forms.ModelForm):
    class Meta:
        model = TwitchalertsAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color', 'filter_type', 'filter_amount']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

@login_required
def test_alert(request, alert_id=None):
    ac = TwitchalertsAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts', 'amount': '$17.32', 'comment': 'Test Twitchalerts Donation from Livestream Alerts'}, True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/twitchalerts/")

alert_config = ac(
    MODULE_NAME,
    AlertForm,
    TwitchalertsAlertConfig,
    {"alert_text": "[[name]] has donated [[amount]]!"})
