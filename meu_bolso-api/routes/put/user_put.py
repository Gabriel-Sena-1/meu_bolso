from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from model.User import User
from pydantic import BaseModel

router = APIRouter()

# Definindo o modelo Pydantic que será recebido no corpo da requisição (sem id_user)
class UserUpdate(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str

# Rota PUT que recebe o id_user na URL e os dados via corpo da requisição
@router.put("/{id_user}")
def editar_usuario(id_user: int, user_data: UserUpdate):
    # Buscar o usuário existente pelo ID
    usuario_atual = User.buscar_por_id(id_user)
    
    if not usuario_atual:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Criar o objeto User com os dados existentes
    usuario = User(
        nome=user_data.nome,            # Atualiza com os novos dados recebidos
        sobrenome=user_data.sobrenome,
        email=user_data.email,
        senha=user_data.senha,
    )

    # Definir o id_user manualmente após a criação
    usuario.id_user = usuario_atual.id_user

    # Atualizar outros campos mantidos
    usuario.tipo_usuario = usuario_atual.tipo_usuario
    usuario.qtd_grupos = usuario_atual.qtd_grupos
    usuario.ativo = usuario_atual.ativo

    # Salvar as mudanças no banco de dados
    sucesso = usuario.editar()

    if not sucesso:
        raise HTTPException(status_code=400, detail="Falha ao editar o usuário.")
    
    return JSONResponse(content={"status": 200, "message": "Dados atualizados com sucesso.", "usuario": usuario.model_dump()})
