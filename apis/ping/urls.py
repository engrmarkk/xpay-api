from django.urls import path
from apis.ping.views import ping


urlpatterns = [
    path("", ping, name="ping"),
]
