from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from .dowellconnection import dowellconnection
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
    
    if "session_id" in request.session:
        dic = request.session
        session_id = dic["session_id"]
        field = {"SessionID":session_id}
        context= {}
        data = dowellconnection("login","bangalore","login","login","login","6752828281","ABCDE","fetch",field,"nil")
        data1 = json.loads(data)
        lstodic = data1["data"][-1]
        context["username"] = lstodic["Username"]
        
        return render(request, 'home.html', context)
    
    else:
        return redirect("https://100014.pythonanywhere.com/")

    #return render(request, 'home.html')

# Homepage
def main(request):
    
    return render(request, 'main.html')
'''
def roomLink(request):    
    return render(request, 'room-link.html')
'''
        
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