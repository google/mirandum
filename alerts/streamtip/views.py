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

from datetime import  datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import django.forms as forms

from main.support import ac
from streamtip.models import StreamtipUpdate, StreamtipAlertConfig 
from streamtip.signals import config_to_alert

MODULE_NAME = "streamtip"

@login_required
def home(request):
    ffconfigs = StreamtipUpdate.objects.filter(user=request.user)
    alerts = StreamtipAlertConfig.objects.filter(user=request.user)
    return render(request, "streamtip/home.html", {'configs': ffconfigs,
        'alerts': alerts})

class StreamtipForm(forms.Form):
    client_id = forms.CharField()
    access_token = forms.CharField()

@login_required
def setup(request):
    if request.POST:
        f = StreamtipForm(request.POST)
        if f.is_valid():
            ffu = StreamtipUpdate(
                client_id=f.cleaned_data['client_id'], 
                access_token=f.cleaned_data['access_token'], 
                type="streamtip", 
                user=request.user)
            ffu.save()
            return HttpResponseRedirect("/streamtip/")
    else:
        f = StreamtipForm()
    return render(request, "streamtip/setup.html", {'form': f})

class AlertForm(forms.ModelForm):
    class Meta:
        model = StreamtipAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color', 'filter_type', 'filter_amount', 'layout', 'animation_in', 'animation_out', 'font_effect']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

@login_required
def test_alert(request, alert_id=None):
    ac = StreamtipAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts', 'amount': '$17.32', 'comment': 'Test Streamtip Donation from Livestream Alerts'}, True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/streamtip/")

alert_config = ac(
    MODULE_NAME,
    AlertForm,
    StreamtipAlertConfig,
    {"alert_text": "[[name]] has donated [[amount]]!"})
