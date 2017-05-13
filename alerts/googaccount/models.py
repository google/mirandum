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
from oauth2client.contrib.django_orm import CredentialsField
from django.contrib.auth.models import User
   
class AppCreds(models.Model):
  user = models.ForeignKey(User, blank=True, null=True)
  label = models.CharField(max_length=255)
  channel_id = models.CharField(default="", max_length=30)

class CredentialsModel(models.Model):
  id = models.ForeignKey(AppCreds, primary_key=True)
  credential = CredentialsField()
