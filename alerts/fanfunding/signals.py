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
from fanfunding.models import FanFundingEvent, AlertConfig
from donations.support import add_donation
import json
from fanfunding.tts import do_it

def config_to_alert(alert, info, test=False):
    if alert.blacklist:
        blacklist_strings = map(lambda x: x.strip(), alert.blacklist.split(","))
    else:
        blacklist_strings = []
    for s in blacklist_strings:
        if s and s.lower() in info['name'].lower():
            return
    text = alert.alert_text.encode("utf-8")
    text = text.replace("[[name]]", info['name'].encode("utf-8"))
    text = text.replace("[[amount]]", info['amount'].encode("utf-8"))
    text = text.replace("[[comment]]", info['comment'].encode("utf-8"))
    sound_url = alert.sound_url
    if alert.text_to_speech and info['comment']:
        try:
            do_it(alert.sound_url, info['comment'], str(info['id'])) 
            sound_url = "https://www.livestreamalerts.com/static/sounds/%s.wav" % info['id']
        except:
            print "Failed text to speech on %s" % info['id']
    style = AlertStyle(image=alert.image_url, sound=sound_url, font=alert.font, font_size=alert.font_size, font_color=alert.font_color)
    style.save()
    a = Alert(text=text, time=timezone.now(), user=alert.user, style=style, test=test, config=alert)
    a.save()

@receiver(post_save, sender=FanFundingEvent)
def event(instance, **kwargs):
    user = instance.updater.credentials.user
    details = json.loads(instance.details)
    info = instance.as_dict()
    info['id'] = instance.id
    alerts = AlertConfig.objects.filter(user=user).order_by("filter_type", "-filter_amount")
    amount_micros = info['amount_micros']
    for alert in alerts:
        if alert.filter_type == "1equal" and alert.filter_amount:
            if alert.filter_amount * 1000000 == amount_micros:
                config_to_alert(alert, info)
                break
        elif alert.filter_type == "2gt" and alert.filter_amount:
            if alert.filter_amount * 1000000 < amount_micros:
                config_to_alert(alert, info)
                break
        elif alert.filter_type == "3default":
            config_to_alert(alert, info)
    add_donation(instance.as_dict(), user, "fanfunding")


if __name__ == "__main__":
    # simple testing.
    import django
    django.setup()
    event(FanFundingEvent.objects.get(id=2120))
