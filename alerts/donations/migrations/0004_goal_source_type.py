# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='source_type',
            field=models.CharField(default=b'', help_text=b'Limit donations to a specific type of donation for this goal.', max_length=100, choices=[(b'', b'All types'), (b'extralife', b'Extra Life'), (b'fanfunding', b'Fan Funding'), (b'streamtip', b'Stream Tip'), (b'streamjar', b'Stream Jar'), (b'imraising', b'Imraising')]),
        ),
    ]
