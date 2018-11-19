from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from general.views import load_user_context, check_login, load_staff_list_context
from .models import Subforum, Thread, Reply
from .forms import ReplyForm, ThreadForm

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

	t = request.GET.get('t')
	# Redirect to forum if no thread requested
	if t is None:
		return redirect('forum')

	try:
		thread = Thread.objects.get(key=t)
		context['thread'] = thread.__dict__
		context['thread']['file'] = thread.file

		author = thread.author
		context['thread']['author'] = author.__dict__
		context['thread']['author']['avatar'] = author.profile.avatar
		context['thread']['author']['posts'] = get_total_posts(author)

		context['thread']['replies'] = {}
		# context['thread'] = {
		# 	'title': thread.title,
		# 	'date': thread.date,
		# 	'content': thread.content,
		# 	'author': {
		# 		'id': author.id,
		# 		'username': author.username,
		# 		'is_staff': author.is_staff,
		# 		'avatar': author.profile.avatar,
		# 		'posts': get_total_posts(author)
		# 	},
		# 	'replies': {}
		# }
		replies = thread.reply_set.all()
		for reply in replies:
			author = reply.author

			context['thread']['replies'][reply.key] = reply.__dict__

			context['thread']['replies'][reply.key]['author'] = author.__dict__
			context['thread']['replies'][reply.key]['author']['avatar'] = author.profile.avatar
			context['thread']['replies'][reply.key]['author']['posts'] = get_total_posts(author)

			# context['thread']['replies'][reply.key] = {
			# 	'date': reply.date,
			# 	'content': reply.content,
			# 	'author': {
			# 		'id': author.id,
			# 		'username': author.username,
			# 		'is_staff': author.is_staff,
			# 		'avatar': author.profile.avatar,
			# 		'posts': get_total_posts(author)
			# 	}
			# }
		# Load Reply Form
		context['reply_form'] = ReplyForm()
	except Thread.DoesNotExist:
		return redirect('forum')

	return render(request, 'forum/thread.html', context)

def post_thread(request):
	if not check_login(request):
		return redirect('home')

	if request.POST:
		print('ok')

def post_reply(request):
	if not check_login(request):
		return redirect('home')

	if request.POST:
		reply = ReplyForm(request.POST)
		thread_key = request.GET.get('t')

		if reply.is_valid():
			reply = reply.save(commit=False)
			reply.thread = Thread.objects.get(key=thread_key)
			reply.author = User.objects.get(id=request.session['user_id'])
			reply = reply.save()
			response = redirect('thread')
			response['Location'] += '?t=' + thread_key # + "#" + reply.key
			return response

	return redirect('forum')

def get_total_posts(user):
	return user.thread_set.count() + user.reply_set.count()
