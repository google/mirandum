# -*- coding: utf-8 -*-

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

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from main.models import Session
from donations.models import TopList

from donations.support import add_donation, output_for_top

class SimpleTopDonations(TestCase):
    def setUp(self):
        u = User(username="top-donor-1")
        u.save()
        add_donation({
            'name': 'foo',
            'timestamp': timezone.now() - timedelta(seconds=60),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        add_donation({
            'name': 'foo',
            'timestamp': timezone.now() - timedelta(seconds=120),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")

        top = TopList(user=u)
        top.save()

        self.top = top
    
    def testTopOutput(self):
        self.assertEquals("foo: $2.00", output_for_top(self.top))

class DailyTopDonations(TestCase):
    def setUp(self):
        u = User(username="top-donor-2")
        u.save()
        add_donation({
            'name': 'foo',
            'timestamp': timezone.now() - timedelta(seconds=60),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        add_donation({
            'name': 'foo',
            'timestamp': timezone.now() - timedelta(days=5),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")

        top = TopList(user=u, type="limited", days=1)
        top.save()

        self.top = top
    
    def testTopOutput(self):
        self.assertEquals("foo: $1.00", output_for_top(self.top))

class DailyTopDonationsComplex(TestCase):
    def setUp(self):
        u = User(username="top-donor-3")
        u.save()
        add_donation({
            'name': 'foo',
            'timestamp': timezone.now() - timedelta(seconds=60),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        add_donation({
            'name': 'foo',
            'timestamp': timezone.now() - timedelta(days=5),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        add_donation({
            'name': 'bar',
            'timestamp': timezone.now(),
            'comment': '',
            'donation_amount': 5.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        add_donation({
            'name': 'baz 😀 ',
            'timestamp': timezone.now(),
            'comment': '',
            'donation_amount': 4.90,
            'currency': 'EUR'
        }, user=u, type="fanfunding")

        top = TopList(user=u, type="limited", days=1, count=3)
        top.save()

        self.top = top
    
    def testTopOutput(self):
        self.assertEquals("baz 😀 : €4.90, bar: $5.00, foo: $1.00", output_for_top(self.top).encode("utf-8"))

        
class SessionTopDonation(TestCase):
    def setUp(self):
        u = User(username="top-donor-4")
        u.save()
        add_donation({
            'name': '😇',
            'timestamp': timezone.now() - timedelta(seconds=60),
            'comment': '',
            'donation_amount': 1.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")

        add_donation({
            'name': '😇',
            'timestamp': timezone.now() - timedelta(seconds=120),
            'comment': '',
            'donation_amount': 4.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        session = Session(user=u,
            session_start = timezone.now() - timedelta(seconds=90))
        session.save()    

        top = TopList(user=u, type="session")
        top.save()

        self.top = top
    
        u = User(username="top-donor-5")
        u.save()
        add_donation({
            'name': '😇',
            'timestamp': timezone.now() - timedelta(seconds=60),
            'comment': '',
            'donation_amount': 4.00,
            'currency': 'USD'
        }, user=u, type="fanfunding")
        
        top = TopList(user=u, type="session")
        top.save()

        self.top_no_session = top
    def testTopOutput(self):
        self.assertEquals("😇: $1.00", output_for_top(self.top).encode("utf-8"))
        self.assertEquals("😇: $4.00", output_for_top(self.top_no_session).encode("utf-8"))
