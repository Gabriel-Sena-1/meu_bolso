from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from model.User import User

router = APIRouter()

@router.delete("/{id_user}")
def deleta_usuario(id_user: int) -> JSONResponse:
    deleta_usuario = User.deletar_usuario(id_user=id_user)
    if not deleta_usuario:
        raise HTTPException(status_code=404, detail="Houve um problema ao deletar o usuário.")
    return JSONResponse(content={"status": 200, "message": "Sucesso ao deletar o usuário!"})
