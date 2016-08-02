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
from django.conf import settings
import django.forms as forms
from django.utils import timezone

def ac(module_name, form, config, form_sample=None):
    @login_required
    def alert_config(request, alert_id=None):
        from upload.models import Upload
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
        if 'image_url' in f.fields:
            uploads = Upload.objects.filter(user=request.user, type__in=['unknown', 'image'])
            choices = [(None, '(none)')]
            for upload in uploads:
                choices.append((upload.remote_path, upload.to_string()))
            f.fields['image_url'].widget = forms.widgets.Select(choices=choices)
        if 'sound_url' in f.fields:
            uploads = Upload.objects.filter(user=request.user, type__in=['sound', 'unknown'])
            choices = []
            for upload in uploads:
                choices.append((upload.remote_path, upload.to_string()))
            f.fields['sound_url'].widget = forms.widgets.Select(choices=choices)
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

def animations_list(type="in"):
    upper_type = type.title()    
    return (
      ("fade%s" % upper_type, "Fade %s" % upper_type),
      ("fade%sDown" % upper_type, "Fade %s Down" % upper_type),
      ("fade%sDownBig" % upper_type, "Fade %s Down Big" % upper_type),
      ("fade%sLeft" % upper_type, "Fade %s Left" % upper_type),
      ("fade%sLeftBig" % upper_type, "Fade %s Left Big" % upper_type),
      ("fade%sRight" % upper_type, "Fade %s Right" % upper_type),
      ("fade%sRightBig" % upper_type, "Fade %s" % upper_type),
      ("fade%sUp" % upper_type, "Fade %s Up" % upper_type),
      ("fade%sUpBig" % upper_type, "Fade %s Up Big" % upper_type),
    
      ("zoom%s" % upper_type, "Zoom %s" % upper_type),
      ("zoom%sDown" % upper_type, "Zoom %s Down" % upper_type),
      ("zoom%sLeft" % upper_type, "Zoom %s Left" % upper_type),
      ("zoom%sRight" % upper_type, "Zoom %s Right" % upper_type),
      ("zoom%sUp" % upper_type, "Zoom %s Up" % upper_type),
    
      ("bounce%s" % upper_type, "Bounce %s" % upper_type),
      ("bounce%sDown" % upper_type, "Bounce %s Down" % upper_type),
      ("bounce%sLeft" % upper_type, "Bounce %s Left" % upper_type),
      ("bounce%sRight" % upper_type, "Bounce %s Right" % upper_type),
      ("bounce%sUp" % upper_type, "Bounce %s Up" % upper_type),
    
      ("slide%sUp" % upper_type, "Slide %s Up" % upper_type),
      ("slide%sDown" % upper_type, "Slide %s Down" % upper_type),
      ("slide%sLeft" % upper_type, "Slide %s Left" % upper_type),
      ("slide%sRight" % upper_type, "Slide %s Right" % upper_type)
    )
def font_effects():
    return (
        ("shadow", "Normal Shadow"),
        ("anaglyph", "Anaglyph"),
        ("brick-sign", "Brick Sign"),
        ("canvas-print", "Canvas Print"),
        ("crackle", "Crackle"),
        ("decaying", "Decaying"),
        ("destruction", "Destruction"),
        ("distressed", "Distressed"),
        ("distressed-wood", "Distressed Wood"),
        ("emboss", "Emboss"),
        ("fire", "Fire"),
        ("fire-animation", "Fire Animation"),
        ("fragile", "Fragile"),
        ("grass", "Grass"),
        ("ice", "Ice"),
        ("mitosis", "Mitosis"),
        ("neon", "Neon"),
        ("outline", "Outline"),
        ("putting-green", "Putting Green"),
        ("scuffed-steel", "Scuffed Steel"),
        ("splintered", "Splintered"),
        ("static", "Static"),
        ("stonewash", "Stonewash"),
        ("3d", "3d"),
        ("3d-float", "3d Float"),
        ("vintage", "Vintage"),
        ("wallpaper", "Wallpaper"),
    )

def check_google_font(font):
    f = open(settings.FONT_LIST)
    for line in f:
        if line.strip() == font:
            return True
    return False

def update_last_activity(user):
    from main.models import LastActivity
    now = timezone.now()
    lu = LastActivity.objects.filter(user=user)
    if lu.count():
        lu = lu[0]
        lu.timestamp = now
    else:
        lu = LastActivity(user=user, timestamp=now)
    lu.save()
    return True
