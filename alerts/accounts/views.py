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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from googaccount.models import AppCreds
from imraising.models import ImraisingUpdate
from streamtip.models import StreamtipUpdate
from streamjar.models import StreamjarUpdate
from twitchalerts.models import TwitchalertsUpdate


@login_required
def home(request):
  goog_accounts = AppCreds.objects.filter(user=request.user)
  imraising_accounts = ImraisingUpdate.objects.filter(user=request.user)
  streamtip_accounts = StreamtipUpdate.objects.filter(user=request.user)
  streamjar_accounts = StreamjarUpdate.objects.filter(user=request.user)
  twitchalerts_accounts = TwitchalertsUpdate.objects.filter(user=request.user)
  return render(request, "accounts/home.html", {
      'goog_accounts': goog_accounts,
      'imraising_accounts': imraising_accounts,
      'streamjar_accounts': streamjar_accounts,
      'streamtip_accounts': streamtip_accounts,
      'twitchalerts_accounts': twitchalerts_accounts})
