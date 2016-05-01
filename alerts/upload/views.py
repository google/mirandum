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
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import django.forms as forms
from django.contrib.auth.decorators import login_required
from upload.models import Upload
from django.conf import settings
import md5
import boto

class UploadForm(forms.Form):
    file = forms.FileField()

def handle_uploaded_file(f, user):
    gcs_bucket = settings.GCS_BUCKET
    user_key = md5.md5(str(user.username)).hexdigest()
    # Sometimes things have paths in them? Windows used to do this.
    name = f.name.split("/")[-1]
    file_key = "%s/%s" % (user_key, name)
    uri = boto.storage_uri("%s/%s" % (gcs_bucket, file_key), "gs")
    uri.set_contents_from_string(f.read())
    return "http://%s/%s" % (gcs_bucket, file_key)

@login_required
def list(request):
    uploads = Upload.objects.filter(user=request.user)
    return render(request, "upload/list.html", {'uploads': uploads})

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'], request.user)
            local_name = request.FILES['file'].name
            local_name = local_name.split("/")[-1]
            up = Upload(local_name=local_name, remote_path = path, user=request.user)
            up.save()
            return HttpResponseRedirect("/upload/")
    else:
        form = UploadForm()
    return render(request, 'upload/upload.html', {'form': form})
