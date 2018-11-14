from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
import random, os

quotes = ['What you do from here on won\'t serve any purpose. You\'ll never see the bigger picture, and it\'s all your own fault.',
'Where are you right now?', '']
pw = "megumin"

def home(request):
	context = {}
	try:
        # If valid user, load home
		if request.session['user_id'] is not None:
			context['user'] = {
				'id': request.session['user_id'],
				'username': request.session['user_name']
			}
			return render(request, 'chat/home.html', context)
	except KeyError:
		# If not, load login splash
		context['quote'] = gen_quote()
		return render(request, 'chat/auth.html', context)

def chat(request):
    # If GET (id), load chatroom
    if request.GET.get("rm"):
        print(request.GET.get("rm"))
        # TODO Load chat context
        return render(request, 'chat/room.html')

    # If no GET(id) or invalid GET(id), load open chatrooms
    return render(request, 'chat/rooms.html')

def login_view(request):
	if request.session['auth'] == False or request.session['user_id'] is not None:
		return redirect('home')
	return render(request, 'chat/login.html')

def login_user(request):
	if request.session['user_id'] is not None:
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
	if request.session['user_id'] is not None:
		return redirect('home')
	if request.POST:
		print('attempted anon login')
		request.session['anon'] = True
		request.session['user_name'] = 'Anonymous'
		redirect('home')

def auth(request):
	if request.session['auth'] == True:
		return redirect('login')

	if request.POST:
		print('attempted auth')
		# print(get_site_pw())
		if request.POST.get('pw') == pw:
			request.session['auth'] = True
			return redirect('login')
	return redirect('home')

def get_site_pw():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print(dir_path)
	pw_file = open('auth.txt', 'r')
	pw = pw_file.read()
	pw_file.close()
	return pw

def gen_quote():
	return quotes[random.randint(0, len(quotes)-1)]
