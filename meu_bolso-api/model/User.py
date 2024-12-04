from datetime import datetime
from db.database_manager import DatabaseManager
import os
from pydantic import BaseModel

host = str(os.getenv("DB_HOST"))
db = DatabaseManager(host, os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))

class UserBase(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str
    tipo_usuario: int
    qtd_grupos: int
    ativo: bool

class UserResponse(UserBase):
    id_user: int

class User:
    def __init__(self, nome, sobrenome, email, senha):
        self.id_user = None
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha



    def salvar(self):
        db.connect()
        try:
            if self.id_user is None:
                sql = """INSERT INTO usuarios (nome, sobrenome, email, senha) 
                        VALUES (%s, %s, %s, %s)"""
                val = (self.nome, self.sobrenome, self.email, self.senha)
                db.execute(sql, val)
                db.commit()
                self.id_user = db.lastrowid  # Captura o ID gerado para o usuário
                return True  # Retorna sucesso na operação
        except Exception as e:
            db.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao salvar o usuário: {e}")
            return False  # Indica que ocorreu um erro
        finally:
            db.disconnect()

    def editar(self):
        db.connect()
        try:
            if self.id_user is not None:
                sql = """UPDATE usuarios 
                        SET nome = %s, sobrenome = %s, email = %s, senha = %s 
                        WHERE id_user = %s"""
                val = (self.nome, self.sobrenome, self.email, self.senha, self.id_user)
                db.execute(sql, val)
                db.commit()
                return True  # Retorna sucesso na operação
        except Exception as e:
            db.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao atualizar o usuário: {e}")
            return False  # Indica que ocorreu um erro
        finally:
            db.disconnect()


    @staticmethod
    def buscar_por_id(id_user: int) -> UserResponse:
        db.connect()
        sql = "SELECT * FROM usuarios WHERE id_user = %s"
        val = (id_user,)
        db.execute(sql, val)
        result = db.fetchone()
        db.disconnect()

        if result:
            user = UserResponse(
                id_user=result[0],
                nome=result[1],
                sobrenome=result[2],
                email=result[3],
                senha=result[4],
                tipo_usuario=result[5],
                qtd_grupos=result[6],
                ativo=result[7]
            )
            return user

        return None


    @staticmethod
    def buscar_todos():
        db.connect()
        sql = "SELECT * FROM usuarios"
        db.execute(sql)
        results = db.fetchall()
        db.disconnect()
        users = []
        for result in results:
            user = UserResponse(
                id_user=result[0],
                nome=result[1],
                sobrenome=result[2],
                email=result[3],
                senha=result[4],
                tipo_usuario=result[5],
                qtd_grupos=result[6],
                ativo=result[7]
            )
            users.append(user)
        return users


    def atualizar(self):
        if self.id_user is not None:
            db.connect()
            sql = "UPDATE usuarios SET nome = %s, sobrenome = %s, email = %s, senha = %s, tipo_usuario = %s, qtd_grupos = %s, ativo = %s WHERE id_user = %s"
            val = (self.nome, self.sobrenome, self.email, self.senha, self.tipo_usuario, self.qtd_grupos, self.ativo, self.id_user)
            db.execute(sql, val)
            db.commit()
            db.disconnect()

    @staticmethod
    def deletar_usuario(id_user: int):
        if id_user is not None:
            db.connect()
            sql = "UPDATE usuarios SET ativo = 0 WHERE id_user = %s"
            val = (id_user,)
            
            try:
                db.execute(sql, val)
                db.commit()
                
                # Verifica quantas linhas foram afetadas
                if db.rowcount > 0:
                    return True  # A query foi bem-sucedida, pelo menos uma linha foi afetada
                else:
                    return False  # Nenhuma linha foi afetada (ID não encontrado, por exemplo)
            except Exception as e:
                db.rollback()  # Em caso de erro, desfaz a transação
                print(f"Erro ao deletar usuário: {e}")
                return False
            finally:
                db.disconnect()

        