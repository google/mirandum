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
import main.models

class ImraisingUpdate(main.models.Updater):
    api_key = models.CharField(max_length=255)

class ImraisingEvent(main.models.UpdaterEvent):
    details = models.TextField()
    updater = models.ForeignKey(ImraisingUpdate)

class ImraisingAlertConfig(main.models.AlertConfig):
    blacklist = models.TextField(blank=True, null=True)
