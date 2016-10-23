# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patreon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patreonalertconfig',
            name='filter_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='patreonalertconfig',
            name='filter_type',
            field=models.CharField(default=b'3default', help_text=b'When filtering for specific amounts, comparison to use.', max_length=20, choices=[(b'1equal', b'Equals'), (b'2gt', b'Greater than'), (b'3default', b'Default')]),
        ),
    ]
