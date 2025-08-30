from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from api_services.custom_exceptions import CustomException

BASE_PREFIX = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{BASE_PREFIX}/ping/", include("apis.ping.urls")),
    path(f"{BASE_PREFIX}/users/", include("apis.users.urls")),
    path(f"{BASE_PREFIX}/auth/", include("apis.authentication.urls")),
]

handler404 = CustomException.custom_404_view
handler500 = CustomException.custom_500_view
