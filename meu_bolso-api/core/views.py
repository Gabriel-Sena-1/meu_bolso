from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Gasto, Grupo, Usuario
from .serializers import GastoSerializer, GrupoSerializer, UsuarioSerializer, LoginUsuarioSerializer
from .services.gasto_service import GastoService
from .services.grupo_service import GrupoService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login

# Create your views here.

class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todos os gastos",
        responses={200: GastoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo gasto",
        request_body=GastoSerializer,
        responses={201: GastoSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def gastos(self, request, pk=None):
        gastos = GastoService.buscar_por_grupo(pk)
        serializer = GastoSerializer(gastos, many=True)
        return Response(serializer.data)
    
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginUsuarioSerializer  # Serializer simplificado para login
        return UsuarioSerializer  # Serializer padrão para as demais ações

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response({
                'message': 'Login realizado com sucesso',
                'user': self.get_serializer(user).data  # Usa o serializer configurado
            })
        return Response(
            {'error': 'Credenciais inválidas'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
