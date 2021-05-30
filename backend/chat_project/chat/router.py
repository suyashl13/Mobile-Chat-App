from django.urls import path
from .consumer import ChatConsumer

ws_urlpatterns = [
    path('/<str:room_name>/', ChatConsumer.as_asgi())
]
