from django.shortcuts import render, redirect
from chat.models import Room, Message, CsvUpload
from django.http import HttpResponse, JsonResponse
from .dowellconnection import dowellconnection
import json, csv
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
#from django.views.generic.base import RedirectView
#from django.http import HttpResponseRedirect


@csrf_exempt
def main(request):
    session_id = request.GET.get('session_id', None)
    if session_id:
        field={"SessionID":session_id}
        sessions=dowellconnection("login","bangalore","login","login","login","6752828281","ABCDE","fetch",field,"nil")
        session=json.loads(sessions)
        for i in session["data"]:
            username=i["Username"]
        fields={"Username":username}

        usr=dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",fields,"nil")
        #return HttpResponse(usr)
        usrdic=json.loads(usr) # this variable have all user details
        #return HttpResponse(usrdic["data"][0]['Role'])
        for i in usrdic["data"]:
            role=i["Role"]
        fids={"Role":role}
        getRole=dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",fids,"nil")
        forRole=json.loads(getRole)

        #if len(usrdic["data"])>0:
        if len(forRole["data"])>0:
            request.session["user_name"]= username
            request.session["Role"]= role
            return render(request ,'main.html', {'usr_nom': request.session.get("user_name"),
                'role': request.session.get("Role")})
        else:
            return redirect("https://100014.pythonanywhere.com/?code=100069")

    else:
        return redirect("https://100014.pythonanywhere.com/?code=100069")

'''
def rahul(request):
    #return HttpResponse(request.session.get("user_name"))
    context={"user":request.session.get("user_name"), "obj":request.session.items()}
    if request.session.get("user_name"):
        return render(request ,'test.html',context)
    else:
        return redirect("https://100014.pythonanywhere.com/?code=100069")
'''
def logout(request):
    del request.session["user_name"]
    return redirect("https://100014.pythonanywhere.com/?code=100069")

def passage(request):
    return render(request,'home.html')


def room(request, room):
    if request.session.get("user_name"):
        username = request.session.get("user_name")
        room_details = Room.objects.get(name=room)
        message = Message.objects.all()

        return render(request, 'room.html', {
            'room': room,
            'room_details': room_details,
            'message': message,
            'username': username,
        })
    else:
        return redirect("https://100014.pythonanywhere.com/?code=100069")

def pasteLink(request):

    return render(request, 'pastelink.html', {'usr': request.session.get("user_name")})


def stopRoom(request, room):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    room = Room.objects.get(pk=room_id)
    dlt_message = Message.objects.filter(value=message)
    dlt_message.delete()
    dlt_username = Message.objects.filter(user=username)
    dlt_username.delete()
    dlt_roomID =  Message.objects.filter(room=room)
    dlt_roomID.delete()
    return HttpResponse('Room Successfully Stopped!')


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


def checkviewInvite(request):
    if request.session.get("user_name"):
        url = request.GET.get('inviteLink')
        return redirect(url)
    else:
        return redirect("https://100014.pythonanywhere.com/?code=100069")


def checkview(request):
    room = request.POST['room_name']
    username = request.session.get("user_name")
    #username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    #username = request.POST['username']
    username = request.session.get("user_name")
    room_id = request.POST['room_id']
    room = Room.objects.get(pk=room_id)

    new_message = Message.objects.create(value=message, user=username, room=room)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details)
    return JsonResponse({"messages":list(messages.values())})