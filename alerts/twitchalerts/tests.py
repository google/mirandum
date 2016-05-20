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

from django.test import TestCase

from django.utils import timezone
from twitchalerts.models import TwitchalertsUpdate, TwitchalertsEvent
from django.contrib.auth.models import User
from donations.models import Donation
from twitchalerts.support import run_twitchalerts


SAMPLE = {
  "data":[
    {
      "donation_id":"80179029",
      "created_at":"1438576556",
      "currency":"USD",
      "amount":"50",
      "name":"Thomas",
      "message":"nice!"
    }
 ] 
}

class InsertTwitchalertss(TestCase):
    def setUp(self):
        u = User(username="chris-ta")
        u.save()
        updater = TwitchalertsUpdate(access_token = "a", refresh_token="b", refresh_before = timezone.now(), type="twitchalerts", user=u)
        updater.save()
        self.updater = updater

    def testInsertion(self):
        def producer(*args):
            return SAMPLE
        self.assertEqual(Donation.objects.filter(type="twitchalerts").count(), 0)
        run_twitchalerts(self.updater, producer=producer)
        
        self.assertEqual(TwitchalertsEvent.objects.count(), 1)
        self.assertEqual(Donation.objects.filter(type="twitchalerts").count(), 1)
