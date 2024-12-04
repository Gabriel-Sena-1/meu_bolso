from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, GastoViewSet, GrupoViewSet

# Criar o router
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'gastos', GastoViewSet)
router.register(r'grupos', GrupoViewSet)

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]