from rest_framework import serializers, fields
from .models import AudioBook, Song, Podcast, Participant
import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import datetime
import pytz

utc=pytz.UTC

def upload_in_past(UploadedTime):
    right_now=datetime.datetime.now()
    right_now=utc.localize(right_now) 
    if UploadedTime < right_now:
        raise serializers.ValidationError("Upload Time must not be in the past.")

class SongSerializer(serializers.ModelSerializer):
    UploadedTime = fields.DateTimeField(validators=[upload_in_past])
    class Meta:
        model=Song
        fields=('SongID','Name','Duration','UploadedTime')

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Participant
        fields=('id','NameOfTheParticipant','PodcastAppeared')

class PodcastSerializer(serializers.ModelSerializer):
    UploadedTime = fields.DateTimeField(validators=[upload_in_past])
    Participants = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model=Podcast
        fields=('PodcastID','Name','Duration','UploadedTime','Host','Participants')


class AudioBookSerializer(serializers.ModelSerializer):
    UploadedTime = fields.DateTimeField(validators=[upload_in_past])
    class Meta:
        model=AudioBook
        fields=('AudioBookID','Title','Author','Narrator','Duration','UploadedTime')