# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0003_auto_20170521_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='post_text',
            field=models.CharField(help_text=b'e.g. / 3000', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meta',
            name='pre_text',
            field=models.CharField(help_text=b"e.g 'Sub Goal:'", max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meta',
            name='font',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meta',
            name='font_effect',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'shadow', b'Normal Shadow'), (b'anaglyph', b'Anaglyph'), (b'brick-sign', b'Brick Sign'), (b'canvas-print', b'Canvas Print'), (b'crackle', b'Crackle'), (b'decaying', b'Decaying'), (b'destruction', b'Destruction'), (b'distressed', b'Distressed'), (b'distressed-wood', b'Distressed Wood'), (b'emboss', b'Emboss'), (b'fire', b'Fire'), (b'fire-animation', b'Fire Animation'), (b'fragile', b'Fragile'), (b'grass', b'Grass'), (b'ice', b'Ice'), (b'mitosis', b'Mitosis'), (b'neon', b'Neon'), (b'outline', b'Outline'), (b'putting-green', b'Putting Green'), (b'scuffed-steel', b'Scuffed Steel'), (b'splintered', b'Splintered'), (b'static', b'Static'), (b'stonewash', b'Stonewash'), (b'3d', b'3d'), (b'3d-float', b'3d Float'), (b'vintage', b'Vintage'), (b'wallpaper', b'Wallpaper')]),
        ),
        migrations.AlterField(
            model_name='meta',
            name='outline_color',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
