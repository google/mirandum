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
from django.contrib.auth.models import User

class Upload(models.Model):
    def to_string(self):
        if self.external:
            return self.remote_path
        else:
            return self.local_name
    local_name = models.CharField(max_length=20000)
    remote_path = models.CharField(max_length=20000)
    type = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User)
    uploaded = models.DateTimeField(auto_now_add=True)
    external = models.BooleanField(default=False)
