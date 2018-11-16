from django.urls import path
from . import views

urlpatterns = [
    # path('', views.chat, name="chat"),
	# Non-user-accessible
	path('getmsgs/', views.get_messages, name="get-messages"),
	path('msg/', views.send_message, name="send-message"),
]
