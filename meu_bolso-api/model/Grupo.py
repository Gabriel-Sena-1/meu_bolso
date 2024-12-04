from pydantic import BaseModel
from db.database_manager import DatabaseManager
import os

host = str(os.getenv("DB_HOST"))
db = DatabaseManager(host, os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))

class GrupoBase(BaseModel):
    nome: str

class GrupoResponse(GrupoBase):
    id_grupo: int

class Grupo:
    def __init__(self, nome: str, id_grupo: int = None):
        self.id_grupo = id_grupo
        self.nome = nome


    def salvar(self, id_user: int) -> bool:
        db.connect()
        try:
            # Verificar a quantidade de grupos que o usuário pode criar
            sql = "SELECT qtd_grupos FROM usuarios WHERE id_user = %s"
            val = (id_user,)
            db.execute(sql, val)
            result = db.fetchone()

            if not result:
                return False
            
            qtd_grupos = result[0]
            if qtd_grupos <= 0:
                return False  # Usuário não pode criar mais grupos
            
            # Inserir o novo grupo
            sql = "INSERT INTO grupos (nome) VALUES (%s)"
            val = (self.nome,)
            db.execute(sql, val)
            db.commit()

            # Obter o id_grupo do novo grupo inserido
            id_grupo = db.lastrowid

            # Associar o grupo ao usuário
            sql = "INSERT INTO usuario_grupo (id_user, id_grupo) VALUES (%s, %s)"
            val = (id_user, id_grupo)
            db.execute(sql, val)
            db.commit()

            # Atualizar a quantidade de grupos do usuário
            sql = "UPDATE usuarios SET qtd_grupos = qtd_grupos - 1 WHERE id_user = %s"
            val = (id_user,)
            db.execute(sql, val)
            db.commit()

            return True
        
        except Exception as e:
            db.rollback()
            print(f"Erro ao salvar o grupo: {e}")
            return False
        
        finally:
            db.disconnect()

    @staticmethod
    def buscar_por_id(id_grupo: int):
        db.connect()
        try:
            sql = "SELECT * FROM grupos WHERE id_grupo = %s"
            val = (id_grupo,)
            db.execute(sql, val)
            result = db.fetchone()
            if result:
                return Grupo(id_grupo=result[0], nome=result[1])
        finally:
            db.disconnect()
        return None

    @staticmethod
    def buscar_todos():
        db.connect()
        sql = "SELECT * FROM grupos"
        db.execute(sql)
        results = db.fetchall()
        db.disconnect()
        grupos = []
        for result in results:
            grupo = GrupoResponse(
                id_grupo=result[0],
                nome=result[1]
            )
            grupos.append(grupo)
        return grupos

    def atualizar(self) -> bool:
        if self.id_grupo is None:
            return False
        
        db.connect()
        try:
            sql = "UPDATE grupos SET nome = %s WHERE id_grupo = %s"
            val = (self.nome, self.id_grupo)
            db.execute(sql, val)
            db.commit()
            return db.rowcount > 0
        except Exception as e:
            db.rollback()
            print(f"Erro ao atualizar o grupo: {e}")
            return False
        finally:
            db.disconnect()

    @staticmethod
    def deletar_grupo(id_grupo: int) -> bool:
        db.connect()
        try:
            # Deletando o grupo da tabela principal
            sql = "DELETE FROM grupos WHERE id_grupo = %s"
            val = (id_grupo,)
            db.execute(sql, val)
            db.commit()

            # Verificando se alguma linha foi afetada
            if db.rowcount == 0:
                return False

            return True
        
        except Exception as e:
            db.rollback()
            print(f"Erro ao deletar o grupo: {e}")
            return False

        finally:
            db.disconnect()

    @staticmethod
    def associar_usuario(id_grupo: int, id_user: int):
        db.connect()
        sql = "INSERT INTO usuario_grupo (id_user, id_grupo) VALUES (%s, %s)"
        val = (id_user, id_grupo)
        db.execute(sql, val)
        db.commit()
        db.disconnect()

    @staticmethod
    def remover_associacao_usuario(id_grupo: int, id_user: int):
        db.connect()
        sql = "DELETE FROM usuario_grupo WHERE id_user = %s AND id_grupo = %s"
        val = (id_user, id_grupo)
        db.execute(sql, val)
        db.commit()
        db.disconnect()

    @staticmethod
    def buscar_usuarios_associados(id_grupo: int):
        db.connect()
        try:
            sql = """
            SELECT u.id_user, u.nome, u.sobrenome, u.email
            FROM usuarios u
            INNER JOIN usuario_grupo ug ON u.id_user = ug.id_user
            WHERE ug.id_grupo = %s
            """
            val = (id_grupo,)
            db.execute(sql, val)
            results = db.fetchall()
            return [{"id_user": row[0], "nome": row[1], "sobrenome": row[2], "email": row[3]} for row in results]
        finally:
            db.disconnect()

    