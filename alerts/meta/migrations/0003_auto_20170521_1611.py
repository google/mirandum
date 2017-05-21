# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0002_auto_20170521_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='font',
            field=models.CharField(default=b'Impact', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meta',
            name='font_color',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meta',
            name='font_effect',
            field=models.CharField(default=None, max_length=255, null=True, blank=True, choices=[(b'shadow', b'Normal Shadow'), (b'anaglyph', b'Anaglyph'), (b'brick-sign', b'Brick Sign'), (b'canvas-print', b'Canvas Print'), (b'crackle', b'Crackle'), (b'decaying', b'Decaying'), (b'destruction', b'Destruction'), (b'distressed', b'Distressed'), (b'distressed-wood', b'Distressed Wood'), (b'emboss', b'Emboss'), (b'fire', b'Fire'), (b'fire-animation', b'Fire Animation'), (b'fragile', b'Fragile'), (b'grass', b'Grass'), (b'ice', b'Ice'), (b'mitosis', b'Mitosis'), (b'neon', b'Neon'), (b'outline', b'Outline'), (b'putting-green', b'Putting Green'), (b'scuffed-steel', b'Scuffed Steel'), (b'splintered', b'Splintered'), (b'static', b'Static'), (b'stonewash', b'Stonewash'), (b'3d', b'3d'), (b'3d-float', b'3d Float'), (b'vintage', b'Vintage'), (b'wallpaper', b'Wallpaper')]),
        ),
        migrations.AddField(
            model_name='meta',
            name='font_size',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meta',
            name='font_weight',
            field=models.CharField(default=b'normal', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meta',
            name='outline_color',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
    ]
