import json
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase#,APIRequestFactory
from rest_framework import status
from ..models import Song,Podcast,AudioBook,Participant


client = Client()
class GetAudioAPITest1(APITestCase):
        
    def setUp(self):
        self.valid_song = Song.objects.create(
            SongID=1,Name="Apocalypse",Duration="300",UploadedTime="2021-05-20T00:00:23Z"
        )
        self.valid_podcast = Podcast.objects.create(
            PodcastID=1,Name="Becoming Wise",Duration="3000",UploadedTime="2021-05-20T00:00:23Z",Host="Jimmy Carter"
        )
        Participant.objects.create(NameOfTheParticipant="Daniel Craig", PodcastAppeared=self.valid_podcast)
        Participant.objects.create(NameOfTheParticipant="Monica", PodcastAppeared=self.valid_podcast)
        self.valid_audiobook = AudioBook.objects.create(
            AudioBookID=1,Title="Game Of Thrones",Author="George R.R. Martin",Narrator="Morgan Freeman",Duration="3000",UploadedTime="2021-05-20T00:00:23Z"
        )
    
    def test_get_allpodcasts2(self): # Gets all Podcasts
        response = client.get(reverse('getapi', kwargs={"audioFileType":"podcast"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_audio1(self): # Gets the song with specified id
        response = client.get(reverse('getapi', kwargs={"audioFileType":"song","audioFileID": self.valid_song.SongID}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_audio2(self): # Invalid route
        response = client.get(reverse('getapi', kwargs={"audioFileType":"songg","audioFileID": self.valid_song.SongID}))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_get_audio3(self): # Invalid ID
        response = client.get(reverse('getapi', kwargs={"audioFileType":"podcast","audioFileID": 5}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetAudioAPITest2(APITestCase):
    def test_get_allsongs1(self): # Gets all songs but currently there are none
        response = client.get(reverse('getapi', kwargs={"audioFileType":"song"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)