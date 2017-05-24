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
from streamme.models import StreammeUpdate, StreammeAlertConfig 
from streamme.signals import config_to_alert

MODULE_NAME = "streamme"

@login_required
def home(request):
    ffconfigs = StreammeUpdate.objects.filter(user=request.user)
    alerts = StreammeAlertConfig.objects.filter(user=request.user)
    return render(request, "streamme/home.html", {'configs': ffconfigs,
        'alerts': alerts})

def creds_form():
    class CredsForm(forms.Form):
        username = forms.CharField()
    return CredsForm    

@login_required
def setup(request):
    CredsForm = creds_form()
    if request.POST:
        f = CredsForm(request.POST)
        if f.is_valid():
            creds = f.cleaned_data['username']
            ffu = StreammeUpdate(username=creds, type="streamme", user=request.user)
            ffu.save()
            return HttpResponseRedirect("/streamme/")
    else:
        f = CredsForm()
    return render(request, "streamme/setup.html", {'form': f})

class AlertForm(forms.ModelForm):
    class Meta:
        model = StreammeAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color', 'layout', 'animation_in', 'animation_out', 'font_effect']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

@login_required
def test_alert(request, alert_id=None):
    ac = StreammeAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts', 'amount': '$17.32', 'comment': 'Test Donation from Livestream Alerts', 'id': 'tmp-%s' % ac.id}, True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/streamme/")

alert_config = ac(
    MODULE_NAME,
    AlertForm,
    StreammeAlertConfig,
    {"alert_text": "[[name]] has followed."})
