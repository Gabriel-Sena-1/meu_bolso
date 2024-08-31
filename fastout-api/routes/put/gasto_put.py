from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Request(BaseModel):
    image_id: int
    correct_classification: str

@router.put("/grupo/{grupo_id}/gasto/{gasto_id}")
def func1()->str:
    return "essa eh a funcao 1"

