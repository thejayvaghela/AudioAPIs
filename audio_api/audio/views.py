from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song,Podcast,AudioBook,Participant
from .serializers import SongSerializer,PodcastSerializer,AudioBookSerializer,ParticipantSerializer
from rest_framework import status, viewsets
import datetime


@api_view(['GET','POST'])
def CreateAudioAPI(request):
    try:
        song=Song.objects.all()
        s=SongSerializer(song,many=True)
        podcast=Podcast.objects.all()
        p=PodcastSerializer(podcast,many=True)
        audiobook=AudioBook.objects.all()
        a=AudioBookSerializer(audiobook,many=True)
        if request.method=="POST":
            requestForCreate=request.data
            audioFileMetadata=requestForCreate['audioFileMetadata']
            date_format='%d-%m-%Y %H:%M:%S'
            audioFileMetadata['UploadedTime']=datetime.datetime.strptime(audioFileMetadata['UploadedTime'],date_format)
            if requestForCreate['audioFileType'] == "song": # Checks the audio file type and Serializes it
                SONGdata=SongSerializer(data=audioFileMetadata)
                if SONGdata.is_valid():
                    print("VALID")
                    SONGdata.save()
                else:
                    print("IN-VALID")
                    return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif requestForCreate['audioFileType'] == "podcast":
                PODCASTdata=PodcastSerializer(data=audioFileMetadata)
                if PODCASTdata.is_valid():
                    print("VALID")
                    PODCASTdata.save()
                else:
                    print("IN-VALID")
                    return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                participants=audioFileMetadata['Participants']
                print(participants)
                print(audioFileMetadata['PodcastID'])
                if len(participants)>10:
                    return Response({"Sorry":"Maximum 10 Participants Allowed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                for i in participants:
                    participant={
                        'NameOfTheParticipant':i,
                        'PodcastAppeared':audioFileMetadata['PodcastID'],
                    }
                    participant=ParticipantSerializer(data=participant)
                    if participant.is_valid():
                        print("VALID participant")
                        participant.save()
                    else:
                        print("IN-VALID participant")
                        return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif requestForCreate['audioFileType'] == "audiobook":
                AUDIOBOOKdata=AudioBookSerializer(data=audioFileMetadata)
                if AUDIOBOOKdata.is_valid():
                    print("VALID")
                    AUDIOBOOKdata.save()
                else:
                    print("IN-VALID")
                    return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Sorry":"Some Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            x={
                'song':s.data,
                'podcast':p.data,
                'audiobook':a.data,
            }
            return Response(x,status=status.HTTP_200_OK)
        if request.method=="GET":
            x={
                'song':s.data,
                'podcast':p.data,
                'audiobook':a.data,
            }
            return Response(x,status=status.HTTP_200_OK)
    except:
        return Response({"Sorry":"Some Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['PUT'])
def UpdateAudioAPI(request,audioFileType,audioFileID):
    try:
        requested_data=request.data
        date_format='%d-%m-%Y %H:%M:%S'
        requested_data['UploadedTime']=datetime.datetime.strptime(requested_data['UploadedTime'],date_format)
        if audioFileType=="song":
            try:
                song=Song.objects.get(SongID=audioFileID)
            except:
                return Response({"Sorry":"No Records Found"},status=status.HTTP_404_NOT_FOUND)
            if int(requested_data['SongID']) != int(audioFileID):
                return Response({"Sorry":"Change in ID not allowed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_SONG=SongSerializer(song,data=requested_data)
            if update_SONG.is_valid():
                print("VALID")
                update_SONG.save()
                return Response(update_SONG.data,status=status.HTTP_200_OK)
            else:
                print("IN-VALID")
                return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif audioFileType=="podcast":
            try:
                podcast=Podcast.objects.get(PodcastID=audioFileID)
            except:
                return Response({"Sorry":"No Records Found"},status=status.HTTP_404_NOT_FOUND)
            print(requested_data['PodcastID'])
            print(audioFileID)
            if int(requested_data['PodcastID']) != int(audioFileID):
                return Response({"Sorry":"Change in ID not allowed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_PODCAST=PodcastSerializer(podcast,data=request.data)
            if update_PODCAST.is_valid():
                print("VALID")
                update_PODCAST.save()
                new_participants=requested_data['Participants']
                try:
                    participants=Participant.objects.filter(PodcastAppeared=podcast)
                    participants.delete()
                except:
                    pass
                if len(new_participants)>10:
                    return Response({"Sorry":"Maximum 10 Participants Allowed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                for i in new_participants:
                    participant={
                        'NameOfTheParticipant':i,
                        'PodcastAppeared':requested_data['PodcastID'],
                    }
                    participant=ParticipantSerializer(data=participant)
                    if participant.is_valid():
                        print("VALID participant")
                        participant.save()
                    else:
                        print("IN-VALID participant")
                        return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response(update_PODCAST.data,status=status.HTTP_200_OK)
            else:
                print("IN-VALID")
                return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif audioFileType=="audiobook":
            try:
                audiobook=AudioBook.objects.get(AudioBookID=audioFileID)
            except:
                return Response({"Sorry":"No Records Found"},status=status.HTTP_404_NOT_FOUND)
            if int(requested_data['AudioBookID']) != int(audioFileID):
                return Response({"Sorry":"Change in ID not allowed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_AUDIOBOOK=AudioBookSerializer(audiobook,data=requested_data)
            if update_AUDIOBOOK.is_valid():
                print("VALID")
                update_AUDIOBOOK.save()
                return Response(update_AUDIOBOOK.data,status=status.HTTP_200_OK)
            else:
                print("IN-VALID")
                return Response({"Sorry":"Invalid Input"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Sorry":"Invalid Route"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({"Sorry":"Some Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            




@api_view(['DELETE'])
def DeleteAudioAPI(request,audioFileType,audioFileID):
    try:
        if audioFileType=="song":
            try:
                delete_data=Song.objects.get(SongID=audioFileID)
            except:
                return Response({"Sorry":"Song Already Not Present."},status=status.HTTP_404_NOT_FOUND)
        elif audioFileType=="podcast":
            try:
                delete_data=Podcast.objects.get(PodcastID=audioFileID)
            except:
                return Response({"Sorry":"Podcast Already Not Present."},status=status.HTTP_404_NOT_FOUND)
        elif audioFileType=="audiobook":
            try:
                delete_data=AudioBook.objects.get(AudioBookID=audioFileID)
            except:
                return Response({"Sorry":"Audiobook Already Not Present."},status=status.HTTP_404_NOT_FOUND) 
        else:
            return Response({"Sorry":"Invalid Route"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        delete_data.delete()
        x={
            "Data Deleted"
        }    
        return Response(x,status=status.HTTP_200_OK)
    except:
        return Response({"Sorry":"Some Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def GetAudioAPI(request,**route):
    try:
        if len(route)==1:
            if route['audioFileType']=="song":
                song=Song.objects.all()
                if len(song)==0:
                    return Response({"Sorry":"No Records Found For Songs."},status=status.HTTP_404_NOT_FOUND)
                s=SongSerializer(song,many=True)
                x={
                    'song':s.data,
                }
                return Response(x,status=status.HTTP_200_OK)
            elif route['audioFileType']=="podcast":
                podcast=Podcast.objects.all()
                if len(podcast)==0:
                    return Response({"Sorry":"No Records Found For Podcasts."},status=status.HTTP_404_NOT_FOUND)
                p=PodcastSerializer(podcast,many=True)
                x={
                    'podcast':p.data,
                }
                return Response(x,status=status.HTTP_200_OK)
            elif route['audioFileType']=="audiobook":
                audiobook=AudioBook.objects.all()
                if len(audiobook)==0:
                    return Response({"Sorry":"No Records Found For Audiobooks."},status=status.HTTP_404_NOT_FOUND)
                a=AudioBookSerializer(audiobook,many=True)
                x={
                    'audiobook':a.data,
                }
                return Response(x,status=status.HTTP_200_OK)
            else:
                return Response({"Sorry":"Invalid Route"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif len(route)==2:
            print("INSIDE length 2")
            if route['audioFileType']=="song":
                try:
                    song=Song.objects.get(SongID=route['audioFileID'])
                except:
                    return Response({"Sorry":"No Records Found For This Song."},status=status.HTTP_404_NOT_FOUND)
                s=SongSerializer(song)
                x={
                    'song':s.data,
                }
                return Response(x,status=status.HTTP_200_OK)
            elif route['audioFileType']=="podcast":
                try:
                    podcast=Podcast.objects.get(PodcastID=route['audioFileID'])
                except:
                    return Response({"Sorry":"No Records Found For This Podcast."},status=status.HTTP_404_NOT_FOUND)
                p=PodcastSerializer(podcast)
                x={
                    'podcast':p.data,
                }
                return Response(x,status=status.HTTP_200_OK)
            elif route['audioFileType']=="audiobook":
                try:
                    audiobook=AudioBook.objects.get(AudioBookID=route['audioFileID'])
                except:
                    return Response({"Sorry":"No Records Found"},status=status.HTTP_404_NOT_FOUND)
                a=AudioBookSerializer(audiobook)
                x={
                    'audiobook':a.data,
                }
                return Response(x,status=status.HTTP_200_OK)
            else:
                return Response({"Sorry":"Invalid Route"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Sorry":"Invalid Route"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({"Sorry":"Some Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
