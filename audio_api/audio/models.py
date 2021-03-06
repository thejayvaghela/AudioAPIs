from django.db import models


class Song(models.Model):
    SongID=models.PositiveIntegerField(primary_key=True,default=0)
    Name=models.CharField(max_length=100,null=False)
    Duration=models.PositiveIntegerField(null=False)
    UploadedTime=models.DateTimeField(null=False)
    
class Podcast(models.Model):
    PodcastID=models.PositiveIntegerField(primary_key=True,default=0)
    Name=models.CharField(max_length=100,null=False)
    Duration=models.PositiveIntegerField(null=False)
    UploadedTime=models.DateTimeField(null=False)
    Host=models.CharField(max_length=100,null=False)

class AudioBook(models.Model):
    AudioBookID=models.PositiveIntegerField(primary_key=True,default=0)
    Title=models.CharField(max_length=100,null=False)
    Author=models.CharField(max_length=100,null=False)
    Narrator=models.CharField(max_length=100,null=False)
    Duration=models.PositiveIntegerField(null=False)
    UploadedTime=models.DateTimeField(null=False)

class Participant(models.Model):
    NameOfTheParticipant=models.CharField(max_length=100,null=False)
    PodcastAppeared=models.ForeignKey(Podcast,on_delete=models.CASCADE,related_name='Participants')
    
    def __str__(self):
        return self.NameOfTheParticipant

# song
'''
{
    "audioFileType": "song",
    "audioFileMetadata": {
        "SongID": 1,
        "Name": "Blinding Lights",
        "Duration": 50,
        "UploadedTime": "05-05-2021 00:00:00"
    }
}
'''

# podcast
'''
{
    "audioFileType": "podcast",
    "audioFileMetadata": {
        "PodcastID": 1,
        "Name": "Becoming Wise",
        "Duration": 200,
        "UploadedTime": "05-05-2021 00:00:00",
        "Host" : "James Bond",
        "Participants": [
                "Daniel Craig",
                "Jen"
            ]
    }
}
'''

# audiobook
'''
{
    "audioFileType": "audiobook",
    "audioFileMetadata": {
        "AudioBookID": 1,
        "Title": "Game Of Thrones",
        "Author":"George R.R. Martin",
        "Narrator":"Morgan Freeman",
        "Duration": 2000,
        "UploadedTime": "05-05-2021 00:00:00"
    }
}
'''