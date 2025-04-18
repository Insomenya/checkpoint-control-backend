from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API Системы контроля КПП",
      default_version='v1',
      description="REST API для системы контроля КПП.",
      contact=openapi.Contact(email="admin@checkpoint-control.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   patterns=[
       path('auth/', include('authentication.urls')),
       path('', include('organizations.urls')),
       path('', include('checkpoints.urls')),
       path('', include('expeditions.urls')),
       path('', include('confirmations.urls')),
   ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('organizations.urls')),
    path('', include('checkpoints.urls')),
    path('', include('expeditions.urls')),
    path('', include('confirmations.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)) 