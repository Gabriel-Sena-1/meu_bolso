from django.shortcuts import get_object_or_404
from core.models import Gasto, Grupo, UsuarioGrupo
from django.core.exceptions import ValidationError

class GastoService:
    @staticmethod
    def criar_gasto(nome: str, valor: float, data: str, id_user: int, id_grupo: int) -> bool:
        try:
            grupo = get_object_or_404(Grupo, id=id_grupo)
            
            # Criar o gasto
            gasto = Gasto.objects.create(
                nome=nome,
                valor=valor,
                data=data,
                grupo=grupo
            )

            # Associar usuário ao grupo se ainda não estiver
            UsuarioGrupo.objects.get_or_create(
                usuario_id=id_user,
                grupo=grupo
            )

            return True
        except Exception as e:
            print(f"Erro ao salvar o gasto: {e}")
            return False

    @staticmethod
    def buscar_por_id(id_gasto: int):
        return get_object_or_404(Gasto, id=id_gasto)

    @staticmethod
    def buscar_todos():
        return Gasto.objects.all()

    @staticmethod
    def buscar_por_grupo(id_grupo: int):
        return Gasto.objects.filter(grupo_id=id_grupo)

    @staticmethod
    def editar_gasto(id_gasto: int, nome: str, valor: float, data: str) -> bool:
        try:
            gasto = get_object_or_404(Gasto, id=id_gasto)
            gasto.nome = nome
            gasto.valor = valor
            gasto.data = data
            gasto.save()
            return True
        except Exception as e:
            print(f"Erro ao editar o gasto: {e}")
            return False

    @staticmethod
    def deletar_gasto(id_gasto: int) -> bool:
        try:
            gasto = get_object_or_404(Gasto, id=id_gasto)
            gasto.delete()
            return True
        except Exception as e:
            print(f"Erro ao deletar o gasto: {e}")
            return False 