from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name="forum"),
	path('sub/', views.subforum, name="subforum"),
	path('thread/', views.thread, name="thread"),
	# Non-views
	path('post-thread/', views.post_thread, name="post-thread"),
	path('post-reply/', views.post_reply, name="post-reply")
]
