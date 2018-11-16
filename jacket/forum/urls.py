from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name="forum"),
	path('sub/', views.subforum, name="subforum"),
	path('thread/', views.thread, name="thread")
]
