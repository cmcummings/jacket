from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as session_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Room, Message, Announcement
import random, os

quotes = ['What you do from here on won\'t serve any purpose. You\'ll never see the bigger picture, and it\'s all your own fault.',
'Where are you right now?', '']
pw = "megumin"

def home(request):
	context = {}
    # If valid user, load home
	if check_login(request):
		load_user_context(request, context)
		load_announcement_context(request, context)

		return render(request, 'chat/home.html', context)
	else:
		# If not, load login splash
		context['quote'] = gen_quote()
		return render(request, 'chat/auth.html', context)

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

def login_view(request):
	if check_login(request):
		return redirect('home')
	return render(request, 'chat/login.html')

def login_user(request):
	if check_login(request):
		return redirect('home')
	if request.POST:
		print('attempted login')
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			request.session['user_id'] = user.id
			request.session['user_name'] = user.username
			return redirect('home')
		else:
			return redirect('login')

def login_anon(request):
	if check_login(request):
		return redirect('home')
	if request.POST:
		print('attempted anon login')
		request.session['user_id'] = 0
		request.session['user_name'] = 'Anonymous'
		return redirect('home')

def auth(request):
	if request.POST:
		print('attempted auth')
		# print(get_site_pw())
		if request.POST.get('pw') == pw:
			request.session['auth'] = True
			print('auth succ')
			return redirect('login')
	return redirect('home')

def logout(request):
	session_logout(request)
	return redirect('home')

def check_auth(request):
	try:
		if request.session['auth'] == True:
			return True
	except KeyError:
		return False

def check_login(request):
	try:
		if request.session['user_id'] is not None:
			return True
	except KeyError:
		return False

def load_user_context(request, context):
	context['user'] = {
		'id': request.session['user_id'],
		'username': request.session['user_name']
	}

def load_announcement_context(request, context):
	announcements = Announcement.objects.all()
	context['announcements'] = {}
	for announcement in announcements:
		context['announcements'][announcement.date] = announcement.content

def get_site_pw():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print(dir_path)
	pw_file = open('auth.txt', 'r')
	pw = pw_file.read()
	pw_file.close()
	return pw

def gen_quote():
	return quotes[random.randint(0, len(quotes)-1)]
