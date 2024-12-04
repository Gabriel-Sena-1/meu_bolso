from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from model.Grupo import Grupo

router = APIRouter()

# Modelo Pydantic para receber dados
class Request(BaseModel):
    id_grupo: int

# Rota para retornar todos os grupos
@router.get("")
def retorna_todos_grupos() -> JSONResponse:
    try:
        # Busca todos os grupos utilizando um método do modelo Grupo
        todos_grupos = Grupo.buscar_todos()

        if not todos_grupos:
            raise HTTPException(status_code=404, detail="Nenhum grupo encontrado.")

        # Retorna os grupos em formato JSON
        return JSONResponse(content={"status": 200, "resultado": [grupo.model_dump() for grupo in todos_grupos]})

    except Exception as e:
        print(f"Erro ao buscar grupos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# Rota para retornar um grupo específico por ID
@router.get("/{id_grupo}")
def retorna_um_grupo(id_grupo: int) -> JSONResponse:
    try:
        # Busca o grupo pelo ID utilizando um método do modelo Grupo
        grupo = Grupo.buscar_por_id(id_grupo=id_grupo)

        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado.")

        # Retorna o grupo em formato JSON
        return JSONResponse(content={"status": "sucess", "resultado": grupo.model_dump()})

    except Exception as e:
        print(f"Erro ao buscar grupo por ID: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
