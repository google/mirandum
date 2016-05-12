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

from sponsors.models import SponsorUpdate, SponsorEvent
from googaccount.models import AppCreds
from django.contrib.auth.models import User

from sponsors.support import run_sponsors


# Sponsor API response sample.
#{u'etag': u'"kiOs9cZLH2FUp6r6KJ8eyq_LIOk/YRVaTX7Jpd-kpzSP-1EHF3rC5-0"',
# u'items': [{u'etag': u'"kiOs9cZLH2FUp6r6KJ8eyq_LIOk/xNnLbnsZLi2abH6D0oCGtufoQW8"',
#             u'kind': u'youtube#sponsor',
#             u'snippet': {u'channelId': u'UC0kM0b8W3_rQ09ikl3p29pA',
#                          u'sponsorDetails': {u'channelId': u'UCqaIZcc4piZ911yteiPLUWQ',
#                                              u'channelUrl': u'http://www.youtube.com/channel/UCqaIZcc4piZ911yteiPLUWQ',
#                                              u'displayName': u'BTB Gamers',
#                                              u'profileImageUrl': u'https://yt3.ggpht.com/-qiHV-kgBQPw/AAAAAAAAAAI/AAAAAAAAAAA/juihSHWGEC4/s88-c-k-no-rj-c0xffffff/photo.jpg'},
#                          u'sponsorSince': u'2016-05-07T04:49:13.882Z'}}],
# u'kind': u'youtube#sponsorListResponse',
# u'nextPageToken': u'EAU',
# u'pageInfo': {u'resultsPerPage': 5, u'totalResults': 61}}

def create_sponsor(name):
    "Simple testing helper to create a Sponsor object."
    sponsor = {
        'etag': name,
        'kind': 'youtube#sponsor',
        'snippet': {
            'channelId': 'UC%s' % name,
            'sponsorDetails': {
                'channelUrl': 'http://www.youtube.com/channel/UC%s' % name,
                'displayName': name,
                'sponsorSince': '2016-05-07T04:49:13.882Z'
            }

        }
    }
    return sponsor

def create_sponsors(names):
    "Simple testing helper to create a SponsorList object."
    sponsorList = {
        'etag': '',
        'items': [],
        'kind': 'youtube#sponsorListResponse',
        'nextPageToken': 'E',
        'pageInfo': {}
    }
    for name in names:
        sponsorList['items'].append(create_sponsor(name))
    return sponsorList

class InsertSponsors(TestCase):
    def setUp(self):
        u = User(username="chris")
        u.save()
        ac = AppCreds(user=u, label="Bogus")
        ac.save()
        updater = SponsorUpdate(credentials=ac)
        updater.save()
        self.updater = updater

    def testInsertion(self):
        
        def sponsor_data(*args):
            return create_sponsors(['a', 'b'])
        run_sponsors(self.updater, sponsor_data)
        
        def sponsor_data(*args):
            return create_sponsors(['d', 'c', 'a', 'b'])

        run_sponsors(self.updater, sponsor_data)
        self.assertEqual(SponsorEvent.objects.count(), 4, "Additional runs do not recreate the same sponsors; 4 total")
        d_event = SponsorEvent.objects.get(external_id='d')
        c_event = SponsorEvent.objects.get(external_id='c')
        self.assertTrue(c_event.id < d_event.id, 'Insert new sponsors in reverse order')

        run_sponsors(self.updater, sponsor_data)
        self.assertEqual(SponsorEvent.objects.count(), 4, "Additional runs do not recreate the same sponsors; 4 total")
