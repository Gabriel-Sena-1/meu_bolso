from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Determina a URL base baseado no ambiente
if settings.DEBUG:
    url = 'http://127.0.0.1:8000'
else:
    url = 'https://meu-bolso.onrender.com'

schema_view = get_schema_view(
   openapi.Info(
      title="Meu Bolso API",
      default_version='v1',
      description="API para gerenciamento de gastos pessoais",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=url,  # Define a URL base
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)