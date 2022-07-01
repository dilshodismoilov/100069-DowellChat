from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
#import requests

# Create your views here.
'''
def Dowell_Login(username, password):
    url="http://100014.pythonanywhere.com/api/login/"
    userurl="http://100014.pythonanywhere.com/api/user/"
    payload = {
        'username': username,
        'password': password
    }
    with requests.Session() as s:
        p = s.post(url, data=payload)
        if "Username" in p.text:
            return p.text
        else:
            user = s.get(userurl)
            return user.text

r=Dowell_Login()
'''

def home(request):

    return render(request, 'home.html')

# Homepage
def main(request):
    
    return render(request, 'main.html')

def roomLink(request):
    
    return render(request, 'room-link.html')

        
def room(request, room, id):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    message = Message.objects.all()
    
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'message': message  
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})