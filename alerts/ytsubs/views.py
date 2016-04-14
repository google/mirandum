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
from ytsubs.models import SubUpdate, SubAlertConfig 
from googaccount.models import AppCreds
from django.shortcuts import render
from ytsubs.signals import config_to_alert
import django.forms as forms
from django.forms import ModelForm

@login_required
def home(request):
    ffconfigs = SubUpdate.objects.filter(credentials__user=request.user)
    alerts = SubAlertConfig.objects.filter(user=request.user)
    return render(request, "ytsubs/home.html", {'configs': ffconfigs,
        'alerts': alerts})

class CredsChoices(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.label

@login_required
def setup(request):
    
    class CredsForm(forms.Form):
        account = CredsChoices(queryset=AppCreds.objects.filter(user=request.user), empty_label="")
    
    if request.POST:
        f = CredsForm(request.POST)
        if f.is_valid():
            creds = f.cleaned_data['account']
            ffu = SubUpdate(credentials=creds, last_update=datetime(1990,1,1,0,0,0))
            ffu.save()
            return HttpResponseRedirect("/ytsubs/")
    else:
        f = CredsForm()
    return render(request, "ytsubs/setup.html", {'form': f})

class AlertForm(ModelForm):
    class Meta:
        model = SubAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

#class AlertForm(forms.Form):
#    image = forms.CharField(label="Image URL", widget=forms.TextInput(attrs={'size': 50}), required=False)
#    sound = forms.CharField(label="Sound URL", widget=forms.TextInput(attrs={'size': 50}), required=False)
#    alert_string = forms.CharField(label="Alert Text", widget=forms.TextInput(attrs={'size': 50}))
#    blacklist_strings = forms.CharField(label="Blacklisted Words", help_text="Comma separated words which should prevent alerts being triggered.", widget=forms.Textarea, required=False)

@login_required
def test_alert(request, alert_id=None):
    ac = SubAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts'}, test=True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/ytsubs/")

@login_required
def alert_config(request, alert_id=None):
    ac = None
    if alert_id:
        try:
            ac = SubAlertConfig.objects.get(pk=int(alert_id), user=request.user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/ytsubs/')
        if request.POST and 'delete' in request.POST:
            ac.delete()
            return HttpResponseRedirect('/ytsubs/')
    if request.POST:
        f = AlertForm(request.POST, instance=ac)
    else:
        initial = {"alert_string": "[[name]] has subscribed!"}
        if ac:
            f = AlertForm(instance=ac)
        else:
            f = AlertForm(initial=initial)
    if f.is_valid():
        ac = f.save(commit=False)
        ac.type = "ytsubs"
        ac.user = request.user
        ac.save()
        return HttpResponseRedirect("/ytsubs/")
        
    return render(request, "ytsubs/alert.html", {'form': f, 'new': alert_id is None})
