from django.shortcuts import render, redirect
from general.views import load_user_context, check_login, load_staff_list_context
from .models import Subforum, Thread, Reply

def forum(request):
	if not check_login(request):
		return redirect('home')

	context = {}
	load_user_context(request, context)

	context['subforums'] = {}
	subforums = Subforum.objects.all()
	for subforum in subforums:
		try:
			context['subforums'][subforum.category][subforum.key] = {
				'name': subforum.name,
				'description': subforum.description,
				'nsfw': subforum.nsfw,
				'thread_count': subforum.thread_set.count()
			}
		except KeyError:
			context['subforums'][subforum.category] = {
				subforum.key: {
					'name': subforum.name,
					'description': subforum.description,
					'nsfw': subforum.nsfw,
					'thread_count': subforum.thread_set.count()
				}
			}

	return render(request, 'forum/subforums.html', context)

def subforum(request):
	if not check_login(request):
		return redirect('home')

	context = {}
	load_user_context(request, context)
	load_staff_list_context(context)
	print(context['staff'])

	s = request.GET.get('s')
	# Redirect to forum if no sub requested
	if s is None:
		return redirect('forum')

	try:
		subforum = Subforum.objects.get(key=s)
		context['threads'] = {}
		threads = subforum.thread_set.all()
		for thread in threads:
			context['threads'][thread.key] = {
				'title': thread.title,
				'date': thread.date,
				'content': thread.content,
				'author': {
					'id': thread.author.id,
					'username': thread.author.username,
				}
			}
		context['subforum'] = {
			'name': subforum.name,
			'description': subforum.description
		}
	except Subforum.DoesNotExist:
		# Redirect to forum is sub requested does not exist
		return redirect('forum')

	return render(request, 'forum/subforum.html', context)

def thread(request):
	if not check_login(request):
		return redirect('home')

	# TODO load thread

	context = {}
	load_user_context(request, context)
