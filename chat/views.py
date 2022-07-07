from django.shortcuts import render, redirect
from chat.models import Room, Message, CsvUpload
from django.http import HttpResponse, JsonResponse
from .dowellconnection import dowellconnection
import requests, json, io, csv
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm


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

'''
def generateLink(request):
    
    return render()
'''
#Bulk_Cr8
def csv_upload(request):
    room_list = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()            
            obj = CsvUpload.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                for room in enumerate(reader):

                    if len(room) == 0:
                         return HttpResponse('Make sure the file is not empty')
                    else:                       
                        getRoom = Room(name=room[1][0])
                        room_list.append(getRoom)
                        #Room.objects.create(name=room[1][0])
                        #return redirect('/success')
                Room.objects.bulk_create(room_list)
                
                obj.activated = True
                obj.save()
                return redirect('/success')
                             
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def bulkRoomSuccess(request):
    return render(request, 'success.html')

def roomList(request):
    active_rooms = Room.objects.all()
    return render(request, 'room-list.html', {'active_rooms': active_rooms})

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