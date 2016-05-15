from fanfunding.support import run_fan_funding
from fanfunding.models import FanFundingEvent

from ytsubs.support import run_subs
from ytsubs.models import SubEvent

from sponsors.support import run_sponsors
from sponsors.models import SponsorEvent

from streamtip.support import run_streamtip
from streamtip.models import StreamtipEvent

from twitchalerts.support import run_twitchalerts
from twitchalerts.models import TwitchalertsEvent

from imraising.support import run_imraising
from imraising.models import ImraisingEvent

type_data = {
    'fanfunding': {
        'runner': run_fan_funding,
        'prop': 'fanfundingupdate',
        'event': FanFundingEvent,
    },
    'ytsubs': {
        'runner': run_subs,
        'prop': 'subupdate',
        'event': SubEvent,
    },
    'sponsors': {
        'runner': run_sponsors,
        'prop': 'sponsorupdate',
        'event': SponsorEvent,
    },
    'streamtip': {
        'runner': run_streamtip,
        'prop': 'streamtipupdate',
        'event': StreamtipEvent
    },
    'twitchalerts': {
        'runner': run_twitchalerts,
        'prop': 'twitchalertsupdate',
        'event': TwitchalertsEvent,
    },
    'imraising': {
        'runner': run_imraising,
        'prop': 'imraisingupdate',
        'event': ImraisingEvent,
    },
    'donations': {}
}

def type_choices():
    output = []
    for key in type_data:
        output.append((key, key))
    return sorted(output)
