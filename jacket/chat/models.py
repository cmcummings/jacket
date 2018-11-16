from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from general.models import gen_key as gen_room_key
import random

# Chat models
class Room(models.Model):
	key = models.CharField(max_length=10, default=gen_room_key, unique=True)
	name = models.CharField(max_length=35)
	public = models.BooleanField(default=True)

class Message(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
	content = models.TextField(max_length=250)
