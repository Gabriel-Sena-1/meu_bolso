
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from model.Gasto import Gasto

router = APIRouter()

class Request(BaseModel):
    id_grupo: int
    id_gasto: str
    
@router.get("")
def exibe_todos_gastos()->JSONResponse:
    gastos = Gasto.buscar_todos()
    if not gastos:
        raise HTTPException(status_code=404, detail="Nenhum gasto encontrado.")
    gastos = [gasto.model_dump() for gasto in gastos]
    return JSONResponse(content={"status": "sucess", "resultado": gastos})

@router.get("/{id_grupo}")
def exibe_gastos_por_grupo(id_grupo: int)->JSONResponse:
    gastos = Gasto.buscar_por_grupo(id_grupo=id_grupo)
    if not gastos:
        raise HTTPException(status_code=404, detail="Nenhum gasto encontrado nesse grupo.")
    return JSONResponse(content=[gasto.model_dump() for gasto in gastos])



