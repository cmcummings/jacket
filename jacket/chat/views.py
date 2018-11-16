from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Room, Message
import random, os


def chat(request):
	# If GET (id), load chatroom
	requested_room_key = request.GET.get("rm")
	if requested_room_key is not None:
		try:
			room = Room.objects.get(key=requested_room_key)
			# Load messages into context
			context = {
				'room': {
					'key': room.key,
					'name': room.name
				},
				'messages': {}
			}
			messages = room.message_set.all()
			# Load messages
			for message in messages:
				context['messages'][message.id] = message.__dict__
				context['messages'][message.id]['author'] = {
					'username': message.author.username,
					'is_user': message.author.id == request.session['user_id']
				}
			# Render chatroom
			return render(request, 'chat/room.html', context)
		except Room.DoesNotExist:
			return redirect('chat') # Redirect to all open chatrooms

    # If no GET(id) or invalid GET(id), load open chatrooms
	return render(request, 'chat/rooms.html')

def send_message(request):
	if request.POST:
		data = {}

		room = Room.objects.get(key=request.POST.get('room_key'))
		content = request.POST.get('content')
		message = Message(content=content, room=room)
		message.author = User.objects.get(id=request.session['user_id'])

		message.save()
		data['msg'] = 'succ'
		return JsonResponse(data)

def get_messages(request):
	if request.POST:
		data = {
			'messages': {}
		}

		room = Room.objects.get(key=request.POST.get('room_key'))
		messages = room.message_set.all()

		for message in messages:
			data['messages'][message.id] = {
				'content': message.content,
				'date': message.date,
				'author': {
					'username': message.author.username,
					'is_user': message.author.id == request.session['user_id']
				}
			}

		print(data)
		return JsonResponse(data)
