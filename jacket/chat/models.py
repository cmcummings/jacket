from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random

key_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
def gen_room_key():
	key = ''
	for i in range(0, 10):
		key += key_chars[random.randint(0, len(key_chars)-1)]
	return key

class Room(models.Model):
	key = models.CharField(max_length=10, default=gen_room_key, unique=True)
	name = models.CharField(max_length=35)
	public = models.BooleanField(default=True)

class Message(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
	content = models.TextField(max_length=250)

class Announcement(models.Model):
	date = models.DateTimeField(default=timezone.now)
	content = models.TextField(max_length=100)
