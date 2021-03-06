import json
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase#,APIRequestFactory
from rest_framework import status
from ..models import Song,Podcast,AudioBook,Participant


client = Client()
class DeleteSongAPITest(APITestCase):
    
    def setUp(self):
        self.valid_song1 = Song.objects.create(
            SongID=1,Name="Apocalypse",Duration="300",UploadedTime="2021-05-20T00:00:23Z"
        )
    
    def test_delete_song(self): # Deletes the specified song
        response = client.delete(reverse('deleteapi', kwargs={"audioFileType":"song","audioFileID": self.valid_song1.SongID}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_song_invalid1(self): # Song Not Present In the database
        response = client.delete(reverse('deleteapi', kwargs={"audioFileType":"song","audioFileID": 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_song_invalid2(self): # Invalid Route
        response = client.delete(reverse('deleteapi', kwargs={"audioFileType":"songg","audioFileID": 1}))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeletePodcastAPITest(APITestCase):
    
    def setUp(self):
        self.valid_podcast1 = Podcast.objects.create(# Valid Query
            PodcastID=1,Name="Becoming Wise",Duration="3000",UploadedTime="2021-05-20T00:00:23Z",Host="Jimmy Carter"
        )
        Participant.objects.create(NameOfTheParticipant="Daniel Craig", PodcastAppeared=self.valid_podcast1)
        Participant.objects.create(NameOfTheParticipant="Monica", PodcastAppeared=self.valid_podcast1)
    
    def test_delete_podcast(self): # Deletes the specified podcast
        response = client.delete(reverse('deleteapi', kwargs={"audioFileType":"podcast","audioFileID": self.valid_podcast1.PodcastID}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteAudioBookAPITest(APITestCase):
    
    def setUp(self):
        self.valid_audiobook1 = AudioBook.objects.create(
            AudioBookID=1,Title="Game Of Thrones",Author="George R.R. Martin",Narrator="Morgan Freeman",Duration="3000",UploadedTime="2021-05-20T00:00:23Z"
        )
    
    def test_delete_audiobook(self): # Deletes the specified audiobook
        response = client.delete(reverse('deleteapi', kwargs={"audioFileType":"audiobook","audioFileID": self.valid_audiobook1.AudioBookID}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
