from django.db import models
from django.utils import timezone
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
