from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Action(models.Model):
    user = models.ForeignKey(User)
    action_type = models.CharField(max_length=50,
        choices = (
            ('send_youtube_message', "Send YouTube Message"),
        )
    )
    data = models.TextField()
    use_bot = models.BooleanField(default=False)
