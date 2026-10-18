from django.urls import path
from . import views
from . import chatbot_views

urlpatterns = [
    path('', views.home, name="home"),
    path("chatbot/api/", chatbot_views.chatbot_api, name="chatbot_api"),
]