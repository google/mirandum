from django.shortcuts import render
from meta.models import Meta
from meta.updater import update_meta
from meta.forms import MetaForm
from main.models import AccessKey
from googaccount.models import AppCreds
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect

def output_for_meta(meta):
    pre_text = meta.pre_text or ""
    post_text = meta.post_text or ""
    if pre_text:
        pre_text = u"%s " % pre_text
    if post_text:
        post_text = u" %s" % post_text
    return u"%s%s%s" % (pre_text, meta.counter, post_text)

# Create your views here.

@login_required
def setup(request):
    if request.method == "POST":
        m = Meta(
            appcreds = AppCreds.objects.get(pk=int(request.POST['id'])),
            type = request.POST['type'],
            next_update = timezone.now(),
            last_update = timezone.now(),
            user = request.user
        )
        m.save()
        update_meta(m)
    key = AccessKey.objects.get(user=request.user)
    metas = Meta.objects.filter(user=request.user)
    for i in metas:
        i.display = output_for_meta(i)
    appcreds_subs = AppCreds.objects.filter(user=request.user).exclude(id__in=Meta.objects.filter(user=request.user, type="youtubesubs").values_list('appcreds__id', flat=True))
    appcreds_viewers = AppCreds.objects.filter(user=request.user).exclude(id__in=Meta.objects.filter(user=request.user, type="youtubeviewers").values_list('appcreds__id', flat=True))
    appcreds_likes = AppCreds.objects.filter(user=request.user).exclude(id__in=Meta.objects.filter(user=request.user, type="youtubelikes").values_list('appcreds__id', flat=True))
    return render(request, "meta/setup.html", {'metas': metas, 'appcreds_subs': appcreds_subs, 'appcreds_viewers': appcreds_viewers, 'appcreds_likes': appcreds_likes, 'key': key.key})  

@login_required
def meta_config(request, meta_id=None):
    config = Meta
    form = MetaForm
    ac = None
    if meta_id:
        try:
            ac = config.objects.get(pk=int(meta_id), user=request.user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/meta')
        if request.POST and 'delete' in request.POST:
            ac.delete()
            return HttpResponseRedirect('/meta')
    if request.POST:
        f = form(request.POST, instance=ac)
    else:
        if ac:
            f = form(instance=ac)
        else:
            f = form()
    if f.is_valid():
        ac = f.save(commit=False)
        ac.user = request.user
        ac.save()
        return HttpResponseRedirect("/meta/")

    return render(request, "meta/meta_config.html", {'form': f, 'new': meta_id is None})
