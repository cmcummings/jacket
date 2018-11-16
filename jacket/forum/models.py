from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from general.models import gen_key

class Subforum(models.Model):
	key = models.CharField(max_length=10, default=gen_key, unique=True)
	category = models.CharField(max_length=25)
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=250, blank=True)
	nsfw = models.BooleanField(default=False)

class Thread(models.Model):
	key = models.CharField(max_length=10, default=gen_key, unique=True)
	subforum = models.ForeignKey(Subforum, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	date = models.DateTimeField(default=timezone.now)
	content = models.TextField(max_length=1000)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.FileField(blank=True)

class Reply(models.Model):
	key = models.CharField(max_length=10, default=gen_key, unique=True)
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
	content = models.TextField(max_length=1000)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.FileField(blank=True)
