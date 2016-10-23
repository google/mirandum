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

import os
from datetime import  datetime

import httplib2
import json

from django.conf import settings

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import django.forms as forms

from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_orm import Storage

from main.support import ac
from patreon.signals import config_to_alert
from patreon.models import PatreonCredentialsModel, PatreonAppCreds, PatreonUpdate, PatreonAlertConfig
from patreon.forms import CredsChoices, creds_form

MODULE_NAME = "patreon"

@login_required
def home(request):
    ffconfigs = PatreonUpdate.objects.filter(credentials__user=request.user)
    alerts = PatreonAlertConfig.objects.filter(user=request.user)
    return render(request, "patreon/home.html", {'configs': ffconfigs,
        'alerts': alerts})

class AlertForm(forms.ModelForm):
    class Meta:
        model = PatreonAlertConfig
        fields = ['image_url', 'sound_url', 'alert_text', 'blacklist', 'font', 'font_size', 'font_color', 'layout', 'animation_in', 'animation_out', 'font_effect', 'filter_type', 'filter_amount']
        widgets = {
            'image_url': forms.TextInput(attrs={'size': 50}),
            'sound_url': forms.TextInput(attrs={'size': 50}),
            'alert_text': forms.TextInput(attrs={'size': 50}),
        }

@login_required
def test_alert(request, alert_id=None):
    ac = PatreonAlertConfig.objects.get(pk=int(alert_id), user=request.user)
    config_to_alert(ac, {'name': 'Livestream Alerts'}, True)
    if request.GET.get('ret') == 'alerts':
        return HttpResponseRedirect("/alert_page")
    return HttpResponseRedirect("/patreon/")

alert_config = ac(
    MODULE_NAME,
    AlertForm,
    PatreonAlertConfig,
    {"alert_text": "[[name]] is now a Patron!"})

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '.', 'patreon_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope=['users pledges-to-me my-campaign'],
    redirect_uri='%spatreon/oauth2callback' % settings.SERVER_BASE)
FLOW.params['access_type'] = 'offline'
FLOW.params['approval_prompt'] = 'force'

@login_required
def setup(request):
  FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                 request.user.username)
  authorize_url = FLOW.step1_get_authorize_url()
  return HttpResponseRedirect(authorize_url)

@login_required
def auth_return(request):
  if not xsrfutil.validate_token(settings.SECRET_KEY, str(request.GET['state']),
                                 request.user.username):
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.GET)
  http = httplib2.Http()
  http = credential.authorize(http)
  resp, data = http.request("https://api.patreon.com/oauth2/api/current_user")
  data = json.loads(data)
  name = data['data']['attributes'].get("full_name") or "(unnamed)"
  internal_label = "%s-%s" % (request.user.id, name)
  ac = PatreonAppCreds(user=request.user, label=internal_label)
  ac.save()
  storage = Storage(PatreonCredentialsModel, 'id', ac, 'credential')
  storage.put(credential)
  pu = PatreonUpdate(credentials=ac, user=request.user, type="patreon")
  pu.save()
  return HttpResponseRedirect("/patreon/")

@login_required
def unlink(request, id):
  ac = PatreonAppCreds.objects.get(user=request.user, id=id)
  updaters = _get_updaters(request.user, ac)
  data = {'account': ac, 'updaters': updaters}
  return render(request, "patreon/unlink.html", data)

@login_required
def unlink_confirm(request, id):
  ac = PatreonAppCreds.objects.get(user=request.user, id=id)

  # Delete updaters
  updaters = _get_updaters(request.user, ac)
  for updater in updaters:
    updater.delete()

  # Delete credential
  storage = Storage(PatreonCredentialsModel, 'id', ac, 'credential')
  storage.delete()

  # Delete AppsCred
  ac.delete()

  return HttpResponseRedirect("/accounts/")

def _get_updaters(user, app_creds):
  return PatreonUpdater.objects.filter(credentials=app_creds)
