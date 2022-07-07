from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create-room/', views.home, name='home'),
    #path('', views.home, name='home'),
    
    #Inaccessibles
    path('<str:room>/', views.room, name='room'),
    #path('checkview', views.checkview, name='checkview'),
    path('create-room/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]


