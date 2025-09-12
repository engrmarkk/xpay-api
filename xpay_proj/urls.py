from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500
from api_services.custom_exceptions import CustomException
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


BASE_PREFIX = "api/v1"

schema_view = get_schema_view(
   openapi.Info(
      title="XPAY API",
      default_version='v1',
      description="API documentation for XPay",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@xpay.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(f"{BASE_PREFIX}/ping/", include("apis.ping.urls")),
    path(f"{BASE_PREFIX}/users/", include("apis.users.urls")),
    path(f"{BASE_PREFIX}/auth/", include("apis.authentication.urls")),

    # Swagger & ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# if settings.DEBUG:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = CustomException.custom_404_view
handler500 = CustomException.custom_500_view
