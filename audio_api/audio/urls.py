from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

# router.register('podcast',views.PodcastViewSet,basename='podcast')
# router.register('participant',views.ParticipantViewSet,basename='participant')


urlpatterns = [
    # path('',include(router.urls)),
    path('createaudioapi/', views.CreateAudioAPI, name='createapi'),
    path('deleteaudioapi/<audioFileType>/<audioFileID>/', views.DeleteAudioAPI, name='deleteapi'),
    path('getaudioapi/', views.GetAudioAPI, name='getapi'),
    path('getaudioapi/<audioFileType>/', views.GetAudioAPI, name='getapi'),
    path('getaudioapi/<audioFileType>/<audioFileID>/', views.GetAudioAPI, name='getapi'),
    path('updateaudioapi/<audioFileType>/<audioFileID>/', views.UpdateAudioAPI, name='updateapi'),
]

