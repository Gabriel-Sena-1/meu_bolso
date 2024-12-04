from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from model.Grupo import Grupo

router = APIRouter()

class Request(BaseModel):
    grupo_id: int

# Rota para deletar um grupo por ID
@router.delete("/{grupo_id}")
def deleta_grupo(grupo_id: int) -> JSONResponse:
    try:
        # Inicia a transação de exclusão do grupo
        sucesso = Grupo.deletar_grupo(id_grupo=grupo_id)

        if not sucesso:
            raise HTTPException(status_code=404, detail="Grupo não encontrado ou não pôde ser excluído.")

        return JSONResponse(content={"status": 200, "message": "Grupo excluído com sucesso!"})

    except Exception as e:
        print(f"Erro ao deletar grupo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
