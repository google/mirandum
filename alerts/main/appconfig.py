from fanfunding.support import run_fan_funding
from fanfunding.models import FanFundingEvent

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

from extralife.support import run_extralife
from extralife.models import ExtralifeEvent

from imraising.support import run_imraising
from imraising.models import ImraisingEvent

from youtubesubs.support import run_youtubesubs
from youtubesubs.models import YoutubeSubEvent

from patreon.support import run_patreon
from patreon.models import PatreonEvent

from streamme.support import run_streamme
from streamme.models import StreammeEvent

from beam.support import run_beam
from beam.models import BeamEvent

type_data = {
    'fanfunding': {
        'runner': run_fan_funding,
        'prop': 'fanfundingupdate',
        'event': FanFundingEvent,
        'label': 'Fan Funding',
    },
    'extralife': {
        'runner': run_extralife,
        'prop': 'extralifeupdate',
        'event': ExtralifeEvent,
        'label': 'Extra Life',
    },
    'streamme': {
        'runner': run_streamme,
        'prop': 'streammeupdate',
        'event': StreammeEvent,
        'label': 'Stream.me',
    },
    'beam': {
        'runner': run_beam,
        'prop': 'beamupdate',
        'event': BeamEvent,
        'label': 'Beam',
    },
    'youtubesubs': {
        'runner': run_youtubesubs,
        'prop': 'youtubesubupdate',
        'event': YoutubeSubEvent,
        'label': 'YouTube Subscribers',
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
        'label': 'Streamlabs',
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
    'patreon': {
        'runner': run_patreon,
        'prop': 'patreonupdate',
        'event': PatreonEvent,
        'label': 'Patreon',
    },
    'donations': {
        'label': 'Overall Donations'
    }
}

def type_choices():
    output = []
    for key in type_data:
        if 'donations' == key: continue
        output.append((key, type_data[key].get('label',key)))
    output = sorted(output)
    output = [
        ('donations', 'Overall Donations'),
        ('follows', 'Overall Followers'),
    ] + output
    return output
