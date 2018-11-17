from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Generates a string of 10 random characters
# For some reason Django won't let me change the name of this function,
# so it's just gen_room_key even though its used by other models
key_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
def gen_key():
	key = ''
	for i in range(0, 10):
		key += key_chars[random.randint(0, len(key_chars)-1)]
	return key


# General site models
class Announcement(models.Model):
	date = models.DateTimeField(default=timezone.now)
	content = models.TextField(max_length=100)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	avatar = models.ImageField(upload_to="avatars/", blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
