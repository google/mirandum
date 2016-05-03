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

from django.db.models.signals import post_save
from django.utils import timezone
from main.models import Alert
from django.dispatch import receiver
from main.models import AlertStyle, Alert
from ytsubs.models import SubEvent, SubAlertConfig
import json

def config_to_alert(alert, info, test=False):
    add = True
    if alert.blacklist:
        blacklist_strings = map(lambda x: x.strip(), alert.blacklist.split(","))
    else:
        blacklist_strings = []
    for s in blacklist_strings:
        if s.lower() in info['name'].lower():
            return
    text = alert.alert_text
    text = text.replace("[[name]]", info['name'])
    text += "[[br]]"
    style = AlertStyle(image=alert.image_url, sound=alert.sound_url, font=alert.font, font_size=alert.font_size, font_color=alert.font_color)
    style.save()
    a = Alert(text=text, time=timezone.now(), user=alert.user, style=style, test=test, config=alert)
    a.save()

@receiver(post_save, sender=SubEvent)
def event(instance, **kwargs):
    user = instance.update.credentials.user
    if SubEvent.objects.filter(update=instance.update, details=instance.details).count() > 1:
        # No unsub/resub
        return
    alerts = SubAlertConfig.objects.filter(user=user)
    info = {
        'name': instance.details,
    }
    for alert in alerts:
        config_to_alert(alert, info)
