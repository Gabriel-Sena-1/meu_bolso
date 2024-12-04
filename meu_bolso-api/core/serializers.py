from rest_framework import serializers
from .models import Usuario, Grupo, Gasto

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'nome', 'sobrenome', 'password', 'tipo_usuario', 'qtd_grupos']
        extra_kwargs = {
            'password': {'write_only': True}  # Garante que a senha não seja retornada nas respostas
        }

    def create(self, validated_data):
        # Cria um usuário com senha criptografada
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nome=validated_data.get('nome', ''),
            sobrenome=validated_data.get('sobrenome', ''),
            tipo_usuario=validated_data.get('tipo_usuario', 1),
            qtd_grupos=validated_data.get('qtd_grupos', 3)
        )
        return user

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nome']
        read_only_fields = ['id']

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = ['id', 'nome', 'valor', 'data', 'grupo']
        read_only_fields = ['id'] 