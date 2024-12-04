from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from model.Grupo import Grupo

router = APIRouter()

class GrupoUpdate(BaseModel):
    nome: str

@router.put("/{id_grupo}")
def atualizar_grupo(id_grupo: int, grupo_data: GrupoUpdate, id_user: int):
    try:
        # Buscar o grupo pelo ID
        grupo_existente = Grupo.buscar_por_id(id_grupo)
        if not grupo_existente:
            raise HTTPException(status_code=404, detail="Grupo não encontrado.")
        
        # Verificar se o usuário está associado ao grupo
        usuarios_associados = Grupo.buscar_usuarios_associados(id_grupo)
        usuarios_associados_ids = [usuario["id_user"] for usuario in usuarios_associados]
        if id_user not in usuarios_associados_ids:
            raise HTTPException(status_code=403, detail="Usuário não tem permissão para atualizar este grupo.")

        # Atualizar os dados do grupo
        grupo = Grupo(id_grupo=id_grupo, nome=grupo_data.nome)
        sucesso = grupo.atualizar()

        if not sucesso:
            raise HTTPException(status_code=400, detail="Falha ao atualizar o grupo.")

        return JSONResponse(content={"status": 200, "message": "Grupo atualizado com sucesso.", "grupo": grupo.model_dump()})
    except Exception as e:
        print(f"Erro ao atualizar o grupo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
