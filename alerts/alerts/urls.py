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
    url(r'^$', 'main.views.splash', name='splash'),
    url(r'^home/$', 'main.views.home', name='home_quiet'),
    url(r'^contact/$', 'main.views.contact', name='contact'),
    url(r'^accounts/profile/$', 'main.views.home_redirect', name='home_redirect'),
    url(r'^delete_updater/(?P<id>[0-9]+)$', 'main.views.delete_updater', name='delete_updater'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^stream1/$', RedisQueueView.as_view(redis_channel="foo"), name="stream1"),
    url(r'^alert_page$', 'main.views.alert_page', name='alert_page'),
    url(r'^alert_api$', 'main.views.alert_api', name='alert_api'),
    url(r'^alert_popup$', 'main.views.alert_popup', name='alert_popup'),
    url(r'^reset_key$', 'main.views.reset_key', name='reset_key'),
    url(r'^recent_api$', 'main.views.recent_api'),
    url(r'^recent_api_all$', 'main.views.all_recents'),
    url(r'^recent_config$', 'main.views.recent_config'),
    url(r'^recent_config/(?P<recent_id>[0-9]+)$', 'main.views.recent_config'),
    url(r'^recent_popup$', 'main.views.recent_popup', name='recent_popup'),
    url(r'^label_manager$', 'main.views.label_manager', name='label_manager'),
    url(r'^lists$', 'main.views.lists', name='lists'),
    url(r'^reset_session$', 'main.views.reset_session', name='reset_session'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/$', 'accounts.views.home'),
    
    url(r'^googleaccount/unlink/(?P<id>[0-9]+)', 'googaccount.views.unlink'),
    url(r'^googleaccount/unlink_confirm/(?P<id>[0-9]+)', 'googaccount.views.unlink_confirm'),
    url(r'^googleaccount/setup', 'googaccount.views.setup'),
    url(r'^googleaccount/oauth2callback', 'googaccount.views.auth_return'),
    url(r'^googleaccount/finalize', 'googaccount.views.finalize'),
    url(r'^googleaccount/update_channel/(?P<id>[0-9]+)', 'googaccount.views.update_channel'),
    
    url(r'^twitchaccount/unlink/(?P<id>[0-9]+)', 'twitchaccount.views.unlink'),
    url(r'^twitchaccount/unlink_confirm/(?P<id>[0-9]+)', 'twitchaccount.views.unlink_confirm'),
    url(r'^twitchaccount/setup', 'twitchaccount.views.setup'),
    url(r'^twitchaccount/oauth2callback', 'twitchaccount.views.auth_return'),
    url(r'^twitchaccount/finalize', 'twitchaccount.views.finalize'),
    
    url(r'^extralife/$', 'extralife.views.home'),
    url(r'^extralife/setup$', 'extralife.views.setup'),
    url(r'^extralife/test_alert/(?P<alert_id>[0-9]*)$', 'extralife.views.test_alert'),
    url(r'^extralife/alert$', 'extralife.views.alert_config'),
    url(r'^extralife/alert/(?P<alert_id>[0-9]*)$', 'extralife.views.alert_config'),
    
    url(r'^streamme/$', 'streamme.views.home'),
    url(r'^streamme/setup$', 'streamme.views.setup'),
    url(r'^streamme/test_alert/(?P<alert_id>[0-9]*)$', 'streamme.views.test_alert'),
    url(r'^streamme/alert$', 'streamme.views.alert_config'),
    url(r'^streamme/alert/(?P<alert_id>[0-9]*)$', 'streamme.views.alert_config'),
    
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
    
    url(r'^streamjar/$', 'streamjar.views.home'),
    url(r'^streamjar/setup$', 'streamjar.views.setup'),
    url(r'^streamjar/test_alert/(?P<alert_id>[0-9]*)$', 'streamjar.views.test_alert'),
    url(r'^streamjar/alert$', 'streamjar.views.alert_config'),
    url(r'^streamjar/alert/(?P<alert_id>[0-9]*)$', 'streamjar.views.alert_config'),
    
    url(r'^imraising/$', 'imraising.views.home'),
    url(r'^imraising/setup$', 'imraising.views.setup'),
    url(r'^imraising/test_alert/(?P<alert_id>[0-9]*)$', 'imraising.views.test_alert'),
    url(r'^imraising/alert$', 'imraising.views.alert_config'),
    url(r'^imraising/alert/(?P<alert_id>[0-9]*)$', 'imraising.views.alert_config'),
    
    url(r'^patreon/unlink/(?P<id>[0-9]+)', 'patreon.views.unlink'),
    url(r'^patreon/unlink_confirm/(?P<id>[0-9]+)', 'patreon.views.unlink_confirm'),
    url(r'^patreon/setup', 'patreon.views.setup'),
    url(r'^patreon/oauth2callback', 'patreon.views.auth_return'),
    url(r'^patreon/$', 'patreon.views.home'),
    url(r'^patreon/setup$', 'patreon.views.setup'),
    url(r'^patreon/test_alert/(?P<alert_id>[0-9]*)$', 'patreon.views.test_alert'),
    url(r'^patreon/alert$', 'patreon.views.alert_config'),
    url(r'^patreon/alert/(?P<alert_id>[0-9]*)$', 'patreon.views.alert_config'),
    
    url(r'^twitchalerts/$', 'twitchalerts.views.home'),
    url(r'^twitchalerts/setup$', 'twitchalerts.views.setup'),
    url(r'^twitchalerts/authorize$', 'twitchalerts.views.setup'),
    url(r'^twitchalerts/test_alert/(?P<alert_id>[0-9]*)$', 'twitchalerts.views.test_alert'),
    url(r'^twitchalerts/alert$', 'twitchalerts.views.alert_config'),
    url(r'^twitchalerts/alert/(?P<alert_id>[0-9]*)$', 'twitchalerts.views.alert_config'),
    url(r'^twitchalerts/update_users$', 'twitchalerts.views.update_users'),
    
    url(r'^twitchfollows/$', 'twitchfollows.views.home'),
    url(r'^twitchfollows/setup$', 'twitchfollows.views.setup'),
    url(r'^twitchfollows/test_alert/(?P<alert_id>[0-9]*)$', 'twitchfollows.views.test_alert'),
    url(r'^twitchfollows/alert$', 'twitchfollows.views.alert_config'),
    url(r'^twitchfollows/alert/(?P<alert_id>[0-9]*)$', 'twitchfollows.views.alert_config'),

    url(r'^sponsors/$', 'sponsors.views.home'),
    url(r'^sponsors/setup$', 'sponsors.views.setup'),
    url(r'^sponsors/test_alert/(?P<alert_id>[0-9]*)$', 'sponsors.views.test_alert'),
    url(r'^sponsors/alert$', 'sponsors.views.alert_config'),
    url(r'^sponsors/alert/(?P<alert_id>[0-9]*)$', 'sponsors.views.alert_config'),

    url(r'^upload/$', 'upload.views.list'),
    url(r'^upload/upload$', 'upload.views.upload'),
    url(r'^upload/delete$', 'upload.views.delete_upload'),

    url(r'^donations/$', 'donations.views.home'),
    url(r'^donations/list$', 'donations.views.list'),
    url(r'^donations/top$', 'donations.views.top_config'),
    url(r'^donations/top/(?P<top_id>[0-9]+)$', 'donations.views.top_config'),
    url(r'^donations/goals$', 'donations.views.list_goals'),
    url(r'^donations/goal_popup$', 'donations.views.goal_popup'),
    url(r'^donations/goal_api$', 'donations.views.goal_api'),
    url(r'^donations/goal$', 'donations.views.goal_config'),
    url(r'^donations/goal/(?P<goal_id>[0-9]+)$', 'donations.views.goal_config'),

    url(r'^ytsubs/$', 'ytsubs.views.home'),
    url(r'^ytsubs/test_alert/(?P<alert_id>[0-9]*)$', 'ytsubs.views.test_alert'),
    url(r'^ytsubs/alert$', 'ytsubs.views.alert_config'),
    url(r'^ytsubs/alert/(?P<alert_id>[0-9]*)$', 'ytsubs.views.alert_config'),
    
    url(r'^youtubesubs/$', 'youtubesubs.views.home'),
    url(r'^youtubesubs/setup$', 'youtubesubs.views.setup'),
    url(r'^youtubesubs/test_alert/(?P<alert_id>[0-9]*)$', 'youtubesubs.views.test_alert'),
    url(r'^youtubesubs/alert$', 'youtubesubs.views.alert_config'),
    url(r'^youtubesubs/alert/(?P<alert_id>[0-9]*)$', 'youtubesubs.views.alert_config'),
    
    url(r'^meta/$', 'meta.views.setup'),
    url(r'^meta/meta$', 'meta.views.meta_config'),
    url(r'^meta/meta/(?P<meta_id>[0-9]+)$', 'meta.views.meta_config'),

    url(r'^actions/go$', 'actions.views.go'),
    url(r'^actions/$', 'actions.views.setup'),
    url(r'^actions/(?P<action_type>[a-z_]*)/?$', 'actions.views.setup'),
    
    url(r'^accounts/', include('registration.backends.simple.urls')),
   url(r'^account/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/account/password/reset/done/'},
        name="password_reset"),
    (r'^account/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^account/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/account/password/done/'}, 
        name="password_reset_confirm"),
    (r'^account/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
)
