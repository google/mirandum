from fanfunding.support import run_fan_funding
from fanfunding.models import FanFundingEvent

from ytsubs.support import run_subs
from ytsubs.models import SubEvent

from sponsors.support import run_sponsors
from sponsors.models import SponsorEvent

from streamjar.support import run_streamjar
from streamjar.models import StreamjarEvent

from streamtip.support import run_streamtip
from streamtip.models import StreamtipEvent

from twitchalerts.support import run_twitchalerts
from twitchalerts.models import TwitchalertsEvent

from twitchfollows.support import run_twitchfollows
from twitchfollows.models import TwitchFollowEvent


from imraising.support import run_imraising
from imraising.models import ImraisingEvent

from youtubesubs.support import run_youtubesubs
from youtubesubs.models import YoutubeSubEvent

type_data = {
    'fanfunding': {
        'runner': run_fan_funding,
        'prop': 'fanfundingupdate',
        'event': FanFundingEvent,
        'label': 'Fan Funding',
    },
    'ytsubs': {
        'runner': run_subs,
        'prop': 'subupdate',
        'event': SubEvent,
        'label': 'YouTube Subscribers (email-based)',
    },
    'youtubesubs': {
        'runner': run_youtubesubs,
        'prop': 'youtubesubupdate',
        'event': YoutubeSubEvent,
        'label': 'YouTube Subscribers (new)',
    },
    'sponsors': {
        'runner': run_sponsors,
        'prop': 'sponsorupdate',
        'event': SponsorEvent,
        'label': 'YouTube Sponsors',
    },
    'streamjar': {
        'runner': run_streamjar,
        'prop': 'streamjarupdate',
        'event': StreamtipEvent,
        'label': 'StreamTip',
    },
    'streamtip': {
        'runner': run_streamtip,
        'prop': 'streamtipupdate',
        'event': StreamtipEvent,
        'label': 'StreamTip',
        'delay': 45,
    },
    'twitchalerts': {
        'runner': run_twitchalerts,
        'prop': 'twitchalertsupdate',
        'event': TwitchalertsEvent,
        'label': 'TwitchAlerts',
    },
    'twitchfollows': {
        'runner': run_twitchfollows,
        'prop': 'twitchfollowupdate',
        'event': TwitchFollowEvent,
        'label': 'Twitch Follow',
        'delay': 60,
    },
    'imraising': {
        'runner': run_imraising,
        'prop': 'imraisingupdate',
        'event': ImraisingEvent,
        'label': 'ImRaising',
    },
    'donations': {
        'label': 'Overall Donations'
    }
}

def type_choices():
    output = []
    for key in type_data:
        output.append((key, type_data[key].get('label',key)))
    return sorted(output)
