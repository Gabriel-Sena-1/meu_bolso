from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from model.Gasto import Gasto

router = APIRouter()

@router.delete("/{id_gasto}")
def deletar_gasto(id_gasto: int) -> JSONResponse:
    sucesso = Gasto.deletar_gasto(id_gasto=id_gasto)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail="Houve um problema ao deletar o gasto.")
    
    return JSONResponse(content={"status": 200, "message": "Sucesso ao deletar o gasto!"})