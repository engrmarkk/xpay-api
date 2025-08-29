"""xpay_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
