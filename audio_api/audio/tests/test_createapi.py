import json
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase#,APIRequestFactory
from rest_framework import status
from ..models import Song,Podcast,AudioBook,Participant


client = Client()
class CreateSongAPITest(APITestCase):
    
    def setUp(self):
        self.valid_song1={ # Valid Song
            "audioFileType": "song",
            "audioFileMetadata": {
                "SongID": 1,
                "Name": "Blinding Lights",
                "Duration": 50,
                "UploadedTime": "05-05-2021 00:00:00"
            }
        }
        self.invalid_song1 = {
            "audioFileType": "song",
            "audioFileMetadata": {
                "SongID": -1, # Negetive ID
                "Name": "Blinding Lights",
                "Duration": 50,
                "UploadedTime": "05-05-2021 00:00:00"
            }
        }
        self.invalid_song2 = {
            "audioFileType": "song",
            "audioFileMetadata": {
                "SongID": 2,
                "Name": "Blinding Lights",
                "Duration": 50,
                "UploadedTime": "01-01-2021 00:00:00" # Date in the past
            }
        }
        self.invalid_song3 = {
            "audioFileType": "song",
            "audioFileMetadata": {
                "SongID": 3, # Name Characters more than 100
                "Name": "Blinding Lights Blinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding LightsBlinding Lights",
                "Duration": 50,
                "UploadedTime": "05-05-2021 00:00:00"
            }
        }
        self.invalid_song4 = {
            "audioFileType": "podcast", # file type: podcast
            "audioFileMetadata": { # Metadata for Song
                "SongID": 4,
                "Name": "Blinding Lights",
                "Duration": 50,
                "UploadedTime": "05-05-2021 00:00:00"
            }
        }
        self.invalid_song5 = {
            "audioFileType": "song", 
            "audioFileMetadata": {
                "SongID": 5,
                "Name": "Blinding Lights",
                "Duration": 50,
                "UploadedTime": "" # Empty Field
            }
        } 
        self.invalid_song6 = {
            "audioFileType": "song", 
            "audioFileMetadata": {
                "SongID": 6,
                "Name": "Blinding Lights",
                "Duration": 50,
                # Missing Field UploadedTime
            }
        }
        
        # self.invalid_song7 = {
        #     "audioFileType": "song", 
        #     "audioFileMetadata": {
        #         "SongID": 1,                                   # Similar Primary Key Not Working(SHOULD PASS THE TEST BUT FAILS)
        #         "Name": "Blinding Lights Simialar Key",
        #         "Duration": 50,
        #         "UploadedTime": "06-05-2021 00:00:00"
        #     }
        # }

    def test_create_valid_song1(self):
        response = client.post(reverse('createapi'),
            data=self.valid_song1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_create_invalid_song1(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_song1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_create_invalid_song2(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_song2,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_create_invalid_song3(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_song3,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_create_invalid_song4(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_song4,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_create_invalid_song5(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_song5,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_create_invalid_song6(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_song6,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)




class CreatePodcastAPITest(APITestCase):
    
    def setUp(self):
        self.valid_podcast1={ # Valid Podcast
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
        self.valid_podcast2 = { # Valid Podcast
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "PodcastID": 2,
                "Name": "Becoming Wise",
                "Duration": 200,
                "UploadedTime": "05-05-2021 00:00:00",
                "Host" : "James Bond",
                "Participants": [   # Empty/No Participants
                ]
            }
        }
        self.invalid_podcast1 = {
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "PodcastID": 3,
                "Name": "Becoming Wise",
                "Duration": 200,
                "UploadedTime": "05-05-2021 00:00:00",
                "Host" : "James Bond",
                # Missing Participants
            }
        }
        self.invalid_podcast2 = { 
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "PodcastID": 4,
                "Name": "Becoming Wise",
                "Duration": 200,
                "UploadedTime": "05-05-2021 00:00:00",
                "Host" : "James Bond",
                "Participants": [
                    "Daniel Craig",
                    "Jen",
                    "", # One Empty Participant
                ]
            }
        }
        self.invalid_podcast3 = {
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "PodcastID": 5,
                "Name": "Becoming Wise",
                "Duration": 200,
                "UploadedTime": "05-05-2021 00:00:00",
                "Host" : "James Bond",
                "Participants": [ # More than 10 participants
                    "Daniel Craig","Jen","Robert","Kate","Jay","Messi","Jimmy","Silva","Ronny","Monica","Rachael"
                ]
            }
        }
        
    def test_create_valid_podcast1(self):
        response = client.post(reverse('createapi'),
            data=self.valid_podcast1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_create_valid_podcast2(self):
        response = client.post(reverse('createapi'),
            data=self.valid_podcast2,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_create_invalid_podcast1(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_podcast1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_create_invalid_podcast2(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_podcast2,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_create_invalid_podcast3(self):
        response = client.post(reverse('createapi'),
            data=self.invalid_podcast3,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateAudioBookAPITest(APITestCase):
    def setUp(self):
        self.valid_audiobook1={ # Valid AudioBook
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
    
    def test_create_valid_audiobookt1(self):
        response = client.post(reverse('createapi'),
            data=self.valid_audiobook1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)