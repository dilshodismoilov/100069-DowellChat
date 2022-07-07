from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from .dowellconnection import dowellconnection
import requests, json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    session_id = request.GET.get('session_id', None)
    field = {"SessionID":session_id}
    usr = dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",field,"nil")
    r = json.loads(usr)
      
    if len(r["data"])<1:
        return redirect("https://100014.pythonanywhere.com/?code=100069")
    else:
        return render(request, 'home.html') 
    
    #return render(request, 'home.html')

# Homepage
def main(request):
    
    return render(request, 'main.html')
        
#def room(request, room, id):
def room(request, room):
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