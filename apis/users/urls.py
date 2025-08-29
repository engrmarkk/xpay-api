from django.urls import path
from apis.users.views import UserOperation

urlpatterns = [
    path("me", UserOperation.as_view(), name="user_operation"),
]
