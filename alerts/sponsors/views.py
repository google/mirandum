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
from sponsors.models import SponsorUpdate, SponsorAlertConfig 
from sponsors.signals import config_to_alert
from googaccount.models import AppCreds
from googaccount.forms import CredsChoices, creds_form

MODULE_NAME = "sponsors"

@login_required
def home(request):
    ffconfigs = SponsorUpdate.objects.filter(credentials__user=request.user)
    alerts = SponsorAlertConfig.objects.filter(user=request.user)
    return render(request, "sponsors/home.html", {'configs': ffconfigs,
        'alerts': alerts})

@login_required
def setup(request):
    cred_count = AppCreds.objects.filter(user=request.user).count()
    ffu_count = SponsorUpdate.objects.filter(user=request.user).count()
    if cred_count == 1 and ffu_count == 0:
        creds = AppCreds.objects.get(user=request.user)
        ffu = SponsorUpdate(credentials=creds, type="sponsors", user=request.user)
        ffu.save()
        return HttpResponseRedirect("/sponsors/")
    CredsForm = creds_form(request.user)
    if request.POST:
        f = CredsForm(request.POST)
        if f.is_valid():
            creds = f.cleaned_data['account']
            ffu = SponsorUpdate(credentials=creds, type="sponsors", user=request.user)
            ffu.save()
            return HttpResponseRedirect("/sponsors/")
    else:
        f = CredsForm()
    cred_count = AppCreds.objects.filter(user=request.user).count()
    if cred_count == 0:
        return HttpResponseRedirect("/googleaccount/setup?redir=sponsors")
    return render(request, "sponsors/setup.html", {'form': f, 'count': cred_count})

class AlertForm(forms.ModelForm):
    class Meta:
        model = SponsorAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color', 'layout', 'animation_in', 'animation_out', 'font_effect']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

@login_required
def test_alert(request, alert_id=None):
    ac = SponsorAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts'}, True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/sponsors/")

alert_config = ac(
    MODULE_NAME,
    AlertForm,
    SponsorAlertConfig,
    {"alert_text": "[[name]] is now a sponsor!"})
