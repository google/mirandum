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

from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def ac(module_name, form, config, form_sample=None):
    @login_required
    def alert_config(request, alert_id=None):
        ac = None
        if alert_id:
            try:
                ac = config.objects.get(pk=int(alert_id), user=request.user)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/%s/' % module_name)
            if request.POST and 'delete' in request.POST:
                ac.delete()
                return HttpResponseRedirect('/%s/' % module_name)
        if request.POST:
            f = form(request.POST, instance=ac)
        else:
            initial = form_sample
            if ac:
                f = form(instance=ac)
            else:
                f = form(initial=initial)
        if f.is_valid():
            ac = f.save(commit=False)
            ac.type = module_name
            ac.user = request.user
            ac.save()
            return HttpResponseRedirect("/%s/" % module_name)
            
        return render(request, "%s/alert.html" % module_name, {'form': f, 'new': alert_id is None})
    return alert_config

def formatter(format, data):
    for k, v in data.items():
        if type(v) not in [str, unicode]:
            v = str(v)
        format = format.replace("[[%s]]" % k, v)
    return format
