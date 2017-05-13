from django.shortcuts import render
from meta.models import Meta
from meta.updater import update_meta
from googaccount.models import AppCreds
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.

@login_required
def setup(request):
    if request.method == "POST":
        m = Meta(
            appcreds = AppCreds.objects.get(pk=int(request.POST['id'])),
            type = request.POST['type'],
            next_update = timezone.now(),
            last_update = timezone.now()
        )
        m.save()
        update_meta(m)
        return HttpResponseRedirect("/meta/")
    return render(request, "meta/setup.html")  
