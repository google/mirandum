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

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'alerts.views.home', name='home'),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^home/$', 'main.views.home', name='home_quiet'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^stream1/$', RedisQueueView.as_view(redis_channel="foo"), name="stream1"),
    url(r'^alert_page$', 'main.views.alert_page', name='alert_page'),
    url(r'^alert_api$', 'main.views.alert_api', name='alert_api'),
    url(r'^alert_popup$', 'main.views.alert_popup', name='alert_popup'),
    url(r'^reset_key$', 'main.views.reset_key', name='reset_key'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^googleaccount/$', 'googaccount.views.accounts'),
    url(r'^googleaccount/setup', 'googaccount.views.setup'),
    url(r'^googleaccount/oauth2callback', 'googaccount.views.auth_return'),
    url(r'^googleaccount/finalize', 'googaccount.views.finalize'),
    
    url(r'^fanfunding/$', 'fanfunding.views.home'),
    url(r'^fanfunding/setup$', 'fanfunding.views.setup'),
    url(r'^fanfunding/test_alert/(?P<alert_id>[0-9]*)$', 'fanfunding.views.test_alert'),
    url(r'^fanfunding/alert$', 'fanfunding.views.alert_config'),
    url(r'^fanfunding/alert/(?P<alert_id>[0-9]*)$', 'fanfunding.views.alert_config'),
    
    url(r'^streamtip/$', 'streamtip.views.home'),
    url(r'^streamtip/setup$', 'streamtip.views.setup'),
    url(r'^streamtip/test_alert/(?P<alert_id>[0-9]*)$', 'streamtip.views.test_alert'),
    url(r'^streamtip/alert$', 'streamtip.views.alert_config'),
    url(r'^streamtip/alert/(?P<alert_id>[0-9]*)$', 'streamtip.views.alert_config'),
    
    url(r'^imraising/$', 'imraising.views.home'),
    url(r'^imraising/setup$', 'imraising.views.setup'),
    url(r'^imraising/test_alert/(?P<alert_id>[0-9]*)$', 'imraising.views.test_alert'),
    url(r'^imraising/alert$', 'imraising.views.alert_config'),
    url(r'^imraising/alert/(?P<alert_id>[0-9]*)$', 'imraising.views.alert_config'),

    url(r'^twitchalerts/$', 'twitchalerts.views.home'),
    url(r'^twitchalerts/setup$', 'twitchalerts.views.setup'),
    url(r'^twitchalerts/authorize$', 'twitchalerts.views.setup'),
    url(r'^twitchalerts/test_alert/(?P<alert_id>[0-9]*)$', 'twitchalerts.views.test_alert'),
    url(r'^twitchalerts/alert$', 'twitchalerts.views.alert_config'),
    url(r'^twitchalerts/alert/(?P<alert_id>[0-9]*)$', 'twitchalerts.views.alert_config'),

    url(r'^sponsors/$', 'sponsors.views.home'),
    url(r'^sponsors/setup$', 'sponsors.views.setup'),
    url(r'^sponsors/test_alert/(?P<alert_id>[0-9]*)$', 'sponsors.views.test_alert'),
    url(r'^sponsors/alert$', 'sponsors.views.alert_config'),
    url(r'^sponsors/alert/(?P<alert_id>[0-9]*)$', 'sponsors.views.alert_config'),

    url(r'^upload/$', 'upload.views.list'),
    url(r'^upload/upload$', 'upload.views.upload'),

    url(r'^ytsubs/$', 'ytsubs.views.home'),
    url(r'^ytsubs/setup$', 'ytsubs.views.setup'),
    url(r'^ytsubs/test_alert/(?P<alert_id>[0-9]*)$', 'ytsubs.views.test_alert'),
    url(r'^ytsubs/alert$', 'ytsubs.views.alert_config'),
    url(r'^ytsubs/alert/(?P<alert_id>[0-9]*)$', 'ytsubs.views.alert_config'),
    
    url(r'^accounts/', include('registration.backends.simple.urls')),

)
