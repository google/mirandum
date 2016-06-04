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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from donations.forms import TopForm
from donations.models import Donation, TopList
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

@login_required
def list(request):
    donations = Donation.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "donations/list.html", {'donations': donations})

@login_required
def top_config(request, top_id=None):
    config = TopList
    form = TopForm
    ac = None
    if top_id:
        try:
            ac = config.objects.get(pk=int(top_id), user=request.user)
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

    return render(request, "top_config.html", {'form': f, 'new': top_id is None})
