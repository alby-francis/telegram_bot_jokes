from rest_framework import serializers
from .models import CountJokeModel

class CountJokeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CountJokeModel
        fields  = ['user_chat_id','user_id','first_name','fat_count','dumb_count','stupid_count']
        