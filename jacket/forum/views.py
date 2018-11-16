from django.shortcuts import render, redirect
from general.views import load_user_context, check_login

def forum(request):
	if not check_login(request):
		return redirect('home')

	context = {}
	load_user_context(request, context)

	return render(request, 'forum/subforums.html', context)
