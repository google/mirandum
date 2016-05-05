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
from imraising.models import ImraisingUpdate, ImraisingAlertConfig 
from imraising.signals import config_to_alert

MODULE_NAME = "imraising"

@login_required
def home(request):
    ffconfigs = ImraisingUpdate.objects.filter(user=request.user)
    alerts = ImraisingAlertConfig.objects.filter(user=request.user)
    return render(request, "imraising/home.html", {'configs': ffconfigs,
        'alerts': alerts})

class ImraisingForm(forms.Form):
    key = forms.CharField()

@login_required
def setup(request):
    if request.POST:
        f = ImraisingForm(request.POST)
        if f.is_valid():
            key = f.cleaned_data['key']
            ffu = ImraisingUpdate(api_key=key, type="imraising", user=request.user)
            ffu.save()
            return HttpResponseRedirect("/imraising/")
    else:
        f = ImraisingForm()
    return render(request, "imraising/setup.html", {'form': f})

class AlertForm(forms.ModelForm):
    class Meta:
        model = ImraisingAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

@login_required
def test_alert(request, alert_id=None):
    ac = ImraisingAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts', 'amount': '$17.32', 'comment': 'Test Imraising Donation from Livestream Alerts'}, True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/imraising/")

alert_config = ac(
    MODULE_NAME,
    AlertForm,
    ImraisingAlertConfig,
    {"alert_text": "[[name]] has donated [[amount]]!"})
