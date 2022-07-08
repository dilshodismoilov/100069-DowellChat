from django.db import models
from django.utils import timezone
#from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    #room_users = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    
    def __str__(self):
        return self.user

class CsvUpload(models.Model):
    file_name = models.FileField(upload_to='csv')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.id}'
             