from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('enter-room/', views.passage, name='enter-room'),
    #path('rahul/', views.rahul, name='enter-room'),
    path('upload-rooms/', views.csv_upload, name='upload'),
    path('list-rooms/', views.roomList, name='list-rooms'),
    path('logout/', views.logout, name='logout'),
    path('stop-room/<str:room>/', views.stopRoom, name='stop-room'),
    path('paste-room/', views.pasteLink, name='paste-room'),

    #Inaccessibles
    path('<str:room>/', views.room, name='room'),
    path('enter-room/checkview', views.checkview, name='checkview'),
    path('paste-room/checkview-invite', views.checkviewInvite, name='checkview-invite'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('success', views.bulkRoomSuccess, name='success'),

]


