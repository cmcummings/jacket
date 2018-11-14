from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('chat/', views.chat, name="chat"),
	path('login/', views.login_view, name="login"),
	# Non-user-accessible
	path('auth/', views.auth, name="auth"),
	path('login-user/', views.login_user, name="login-user"),
	path('login-anon/', views.login_anon, name="login-anon")
]
