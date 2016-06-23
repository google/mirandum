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
from donations.forms import TopForm, GoalForm
from donations.models import Donation, TopList, Goal
from main.models import AccessKey

from django.db.models import Sum, Max
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse

import json

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

@login_required
def goal_config(request, goal_id=None):
    config = Goal
    form = GoalForm
    ac = None
    if goal_id:
        try:
            ac = config.objects.get(pk=int(goal_id), user=request.user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/donations/goals')
        if request.POST and 'delete' in request.POST:
            ac.delete()
            return HttpResponseRedirect('/donations/goals')
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
        return HttpResponseRedirect("/donations/goals")

    return render(request, "donations/goal_config.html", {'form': f, 'new': goal_id is None, 'media': f.media})

@login_required
def list_goals(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, "donations/goals.html", {'goals': goals})

def goal_api(request):
    if not 'key' in request.GET or not 'id' in request.GET: 
        return HttpResponseBadRequest()
    key = request.GET['key']
    k = AccessKey.objects.get(key=key)
    goal = Goal.objects.get(pk=request.GET['id']) 
    if k.user != goal.user:
        return HttpResponseBadRequest()
    total = Donation.objects.filter(user=k.user, timestamp__gt=goal.start_date).values('user').annotate(total=Sum('primary_amount'))
    total_amount = 0
    if len(total):
        total_amount = total[0]['total']
    output = {
        'end_date': goal.end_date and str(goal.end_date) or None,
        'start_date': str(goal.start_date),
        'target_amount': goal.amount,
        'description': goal.description,
        'amount': total_amount
    }
    output_s = json.dumps(output)
    return HttpResponse(output_s, content_type='text/plain')

def goal_popup(request):
    return render(request, "donations/goal_page.html")
