from django.db import models
from googaccount.models import AppCreds

class Meta(models.Model):
    appcreds = models.ForeignKey(AppCreds)
    counter = models.IntegerField(default=0)
    type = models.CharField(max_length=50)
    next_update = models.DateTimeField()
    last_update = models.DateTimeField()
