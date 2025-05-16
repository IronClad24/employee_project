# employee_project/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


schema_view = get_schema_view(
    openapi.Info(
        title="Employee API",
        default_version='v1',
        description="API for managing employees, attendance, and departments",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[TokenAuthentication],
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('employees.urls')),
    path('api/', include('attendance.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns += [
    path('api/token/', obtain_auth_token, name='token_auth'),  # token-based login
]


