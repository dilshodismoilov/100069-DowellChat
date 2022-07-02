from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('room-link/', views.roomLink, name='room-link'),
    path('create-room/', views.home, name='home'),
    #path('', views.home, name='home'),
    
    #Inaccessibles
    path('<str:room>/<int:id>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]

#'/'+room+'/?username='+username

#<url> + randomly generated room id , which will be a alpha numeric value
#room - id
#id - randomly generated id