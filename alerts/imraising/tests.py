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
from imraising.models import ImraisingUpdate, ImraisingEvent
from django.contrib.auth.models import User
from donations.models import Donation
from imraising.support import run_imraising


SAMPLE = [
    {"message": "Welcome back the lovely cpg! Hope you had a fantanbulous time in paris \u2661", "_id": "574cf9d4e088a23b48432234", "nickname": "SCK", "amount": {"display": {"currency": "USD", "total": 4.2}}, "time": "2016-05-31T02:41:24.511Z"},
]
class InsertImraisings(TestCase):
    def setUp(self):
        u = User(username="chris-im")
        u.save()
        updater = ImraisingUpdate(api_key = "a", type="imraising", user=u)
        updater.save()
        self.updater = updater

    def testInsertion(self):
        def producer(*args):
            return SAMPLE
        self.assertEqual(Donation.objects.filter(type="imraising").count(), 0)
        run_imraising(self.updater, producer=producer)
        
        self.assertEqual(ImraisingEvent.objects.count(), 1)
        self.assertEqual(Donation.objects.filter(type="imraising").count(), 1)
