import json
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase#,APIRequestFactory
from rest_framework import status
from ..models import Song,Podcast,AudioBook,Participant


client = Client()
class UpdateSongAPITest(APITestCase):
    
    def setUp(self):
        self.create_valid_song1 = Song.objects.create(
            SongID=1,Name="Apocalypse",Duration="300",UploadedTime="2021-05-20T00:00:23Z"
        )
        self.valid_song1={ # Valid Song
            "SongID": 1,
            "Name": "Blinding Lights",
            "Duration": 50,
            "UploadedTime": "06-05-2021 00:00:00"
        }
        self.valid_song2={ # Valid Song
            "SongID": 2,
            "Name": "Blinding Lights But Different ID",
            "Duration": 500,
            "UploadedTime": "04-05-2021 00:00:00"
        }
        
    def test_update_valid_song1(self):
        response = client.put(reverse('updateapi',
            kwargs={"audioFileType":"song","audioFileID": self.create_valid_song1.SongID}),
            data=self.valid_song1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_update_valid_song1(self):
        response = client.put(reverse('updateapi',
            kwargs={"audioFileType":"song","audioFileID": self.create_valid_song1.SongID}), # Call for song1
            data=self.valid_song2,                                                          # but change the id to 2
            content_type='application/json'                                                 # Same for PODCAST and AUDIOBOOK
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePodcastAPITest(APITestCase):
    
    def setUp(self):
        self.create_valid_podcast1 = Podcast.objects.create(
            PodcastID=1,Name="Becoming Wise",Duration="3000",UploadedTime="2021-05-20T00:00:23Z",Host="Jimmy Carter"
        )
        Participant.objects.create(NameOfTheParticipant="Daniel Craig", PodcastAppeared=self.create_valid_podcast1)
        Participant.objects.create(NameOfTheParticipant="Monica", PodcastAppeared=self.create_valid_podcast1)
        
        self.valid_podcast1={
            "PodcastID": 1,
            "Name": "Becoming Wise",
            "Duration": 20050,
            "UploadedTime": "05-05-2021 00:00:00",
            "Host" : "James Bond",
            "Participants": [
                    "Daniel Craig",
                    "Jen",
                    "Jay"   #Add participants
                ]
        }
        self.valid_podcast2={
            "PodcastID": 1,
            "Name": "Becoming Wise2",
            "Duration": 20050,
            "UploadedTime": "05-05-2021 00:00:00",
            "Host" : "James Bond",
            "Participants": []  # Empty the participants
        }
        
    def test_update_valid_podcast1(self):
        response = client.put(reverse('updateapi',
            kwargs={"audioFileType":"podcast","audioFileID": self.create_valid_podcast1.PodcastID}),
            data=self.valid_podcast1, #Add participants
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_update_valid_podcast1(self):
        response = client.put(reverse('updateapi',
            kwargs={"audioFileType":"podcast","audioFileID": self.create_valid_podcast1.PodcastID}),
            data=self.valid_podcast2, # Empty the participants
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class UpdateSAudioBookAPITest(APITestCase):
    
    def setUp(self):
        self.create_valid_audiobook1 = AudioBook.objects.create(
            AudioBookID=1,Title="Game Of Thrones",Author="George R.R. Martin",Narrator="Morgan Freeman",Duration="3000",UploadedTime="2021-05-20T00:00:23Z"
        )
        self.valid_audiobook1={
            "AudioBookID": 1,
            "Title": "Game Of Palaces",
            "Author":"XYZ",
            "Narrator":"Morgan NotAFreeman",
            "Duration": 200023,
            "UploadedTime": "05-05-2021 00:00:00"
        }
        self.invalid_audiobook2={ #invalid data
            "AudioBookID": 1,
            "Title": "Game Of Thrones",
            "Author":"George R.R. Martin",
            "Narrator":"Morgan Freeman",
            "Duration": 2000,
            "UploadedTime": "" # Empty data
        }
        
    def test_update_valid_audiobook1(self):
        response = client.put(reverse('updateapi',
            kwargs={"audioFileType":"audiobook","audioFileID": self.create_valid_audiobook1.AudioBookID}),
            data=self.valid_audiobook1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_update_valid_audiobook2(self):
        response = client.put(reverse('updateapi',
            kwargs={"audioFileType":"audiobook","audioFileID": self.create_valid_audiobook1.AudioBookID}),
            data=self.invalid_audiobook2, # Enters Empty data
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)