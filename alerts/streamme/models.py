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

from django.db import models
from googaccount.models import AppCreds
import main.models
import json
import iso8601

class StreammeUpdate(main.models.Updater):
    username = models.CharField(max_length=150)

class StreammeEvent(main.models.UpdaterEvent):
    details = models.TextField()
    updater = models.ForeignKey(StreammeUpdate)

    def as_dict(self):
        details = json.loads(self.details)
        info = {
            'id': details['userPublicId'],
            # general 
            'name': details['displayName'] or details['username'],
        }
        return info

class StreammeAlertConfig(main.models.AlertConfig):
    blacklist = models.TextField(blank=True, null=True)
