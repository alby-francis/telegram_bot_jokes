from django.db import models

class CountJokeModel(models.Model):
    user_chat_id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    fat_count = models.IntegerField()
    dumb_count = models.IntegerField()
    stupid_count = models.IntegerField()
    