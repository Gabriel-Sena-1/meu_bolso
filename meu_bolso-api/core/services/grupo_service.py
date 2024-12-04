from django.shortcuts import get_object_or_404
from core.models import Grupo, Usuario, UsuarioGrupo
from django.db import transaction

class GrupoService:
    @staticmethod
    def criar_grupo(nome: str, id_user: int) -> bool:
        try:
            with transaction.atomic():
                usuario = get_object_or_404(Usuario, id=id_user)
                
                if usuario.qtd_grupos <= 0:
                    return False

                grupo = Grupo.objects.create(nome=nome)
                UsuarioGrupo.objects.create(usuario=usuario, grupo=grupo)
                
                usuario.qtd_grupos -= 1
                usuario.save()

                return True
        except Exception as e:
            print(f"Erro ao criar grupo: {e}")
            return False

    @staticmethod
    def buscar_por_id(id_grupo: int):
        return get_object_or_404(Grupo, id=id_grupo)

    @staticmethod
    def buscar_todos():
        return Grupo.objects.all()

    @staticmethod
    def buscar_usuarios_associados(id_grupo: int):
        grupo = get_object_or_404(Grupo, id=id_grupo)
        return grupo.usuarios.all() 