# -*- coding: utf-8 -*-
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
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertconfig',
            name='animation_in',
            field=models.CharField(default=b'fadeIn', max_length=100, null=True, blank=True, choices=[(b'fadeIn', b'Fade In'), (b'fadeInDown', b'Fade In Down'), (b'fadeInDownBig', b'Fade In Down Big'), (b'fadeInLeft', b'Fade In Left'), (b'fadeInLeftBig', b'Fade In Left Big'), (b'fadeInRight', b'Fade In Right'), (b'fadeInRightBig', b'Fade In'), (b'fadeInUp', b'Fade In Up'), (b'fadeInUpBig', b'Fade In Up Big'), (b'zoomIn', b'Zoom In'), (b'zoomInDown', b'Zoom In Down'), (b'zoomInLeft', b'Zoom In Left'), (b'zoomInRight', b'Zoom In Right'), (b'zoomInUp', b'Zoom In Up'), (b'bounceIn', b'Bounce In'), (b'bounceInDown', b'Bounce In Down'), (b'bounceInLeft', b'Bounce In Left'), (b'bounceInRight', b'Bounce In Right'), (b'bounceInUp', b'Bounce In Up'), (b'slideInUp', b'Slide In Up'), (b'slideInDown', b'Slide In Down'), (b'slideInLeft', b'Slide In Left'), (b'slideInRight', b'Slide In Right')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertconfig',
            name='animation_out',
            field=models.CharField(default=b'fadeOut', max_length=100, null=True, blank=True, choices=[(b'fadeOut', b'Fade Out'), (b'fadeOutDown', b'Fade Out Down'), (b'fadeOutDownBig', b'Fade Out Down Big'), (b'fadeOutLeft', b'Fade Out Left'), (b'fadeOutLeftBig', b'Fade Out Left Big'), (b'fadeOutRight', b'Fade Out Right'), (b'fadeOutRightBig', b'Fade Out'), (b'fadeOutUp', b'Fade Out Up'), (b'fadeOutUpBig', b'Fade Out Up Big'), (b'zoomOut', b'Zoom Out'), (b'zoomOutDown', b'Zoom Out Down'), (b'zoomOutLeft', b'Zoom Out Left'), (b'zoomOutRight', b'Zoom Out Right'), (b'zoomOutUp', b'Zoom Out Up'), (b'bounceOut', b'Bounce Out'), (b'bounceOutDown', b'Bounce Out Down'), (b'bounceOutLeft', b'Bounce Out Left'), (b'bounceOutRight', b'Bounce Out Right'), (b'bounceOutUp', b'Bounce Out Up'), (b'slideOutUp', b'Slide Out Up'), (b'slideOutDown', b'Slide Out Down'), (b'slideOutLeft', b'Slide Out Left'), (b'slideOutRight', b'Slide Out Right')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertconfig',
            name='font_effect',
            field=models.CharField(default=b'shadow', max_length=100, null=True, blank=True, choices=[(b'shadow', b'Normal Shadow'), (b'anaglyph', b'Anaglyph'), (b'brick-sign', b'Brick Sign'), (b'canvas-print', b'Canvas Print'), (b'crackle', b'Crackle'), (b'decaying', b'Decaying'), (b'destruction', b'Destruction'), (b'distressed', b'Distressed'), (b'distressed-wood', b'Distressed Wood'), (b'emboss', b'Emboss'), (b'fire', b'Fire'), (b'fire-animation', b'Fire Animation'), (b'fragile', b'Fragile'), (b'grass', b'Grass'), (b'ice', b'Ice'), (b'mitosis', b'Mitosis'), (b'neon', b'Neon'), (b'outline', b'Outline'), (b'putting-green', b'Putting Green'), (b'scuffed-steel', b'Scuffed Steel'), (b'splintered', b'Splintered'), (b'static', b'Static'), (b'stonewash', b'Stonewash'), (b'3d', b'3d'), (b'3d-float', b'3d Float'), (b'vintage', b'Vintage'), (b'wallpaper', b'Wallpaper')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertconfig',
            name='layout',
            field=models.CharField(blank=True, max_length=100, null=True, help_text=b'Alert layout (only available with v2 AlertBox)', choices=[(b'vertical', b'Image above text'), (b'side', b'Image next to text'), (b'above', b'Text on top of image')]),
            preserve_default=True,
        ),
    ]
