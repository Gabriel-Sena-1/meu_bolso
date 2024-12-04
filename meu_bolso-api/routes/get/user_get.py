from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from model.User import User

router = APIRouter()

@router.get("")
def retorna_todos_usuarios() -> JSONResponse:
    usuarios = User.buscar_todos()
    if not usuarios:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return JSONResponse(content={"status": "sucess", "resultado":[user.model_dump() for user in usuarios]})

@router.get("/{id_user}")
def retorna_um_usuario(id_user: int) -> JSONResponse:
    usuario = User.buscar_por_id(id_user=id_user)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return JSONResponse(content={"status": 200, "resultado": usuario.model_dump()})
