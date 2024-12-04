from datetime import datetime
from db.database_manager import DatabaseManager
import os
from pydantic import BaseModel, Field

host = str(os.getenv("DB_HOST"))
db = DatabaseManager(host, os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))

class GastoBase(BaseModel):
    nome: str
    valor: float
    data: datetime

class GastoResponse(BaseModel):
    id_gasto: int
    nome: str
    valor: float
    data: str = Field(..., description="Data do gasto em formato ISO")

class Gasto:
    def __init__(self, nome: str, valor: float, data: str):
        self.id_gasto = None
        self.nome = nome
        self.valor = valor
        self.data = data

    def salvar_gasto(self, id_user: int, id_grupo: int):
        db.connect()
        try:
            # Salvando o gasto
            if self.id_gasto is None:
                sql = "INSERT INTO gastos (nome, valor, data) VALUES (%s, %s, %s)"
                val = (self.nome, self.valor, self.data)
                db.execute(sql, val)
                db.commit()
                self.id_gasto = db.lastrowid  # Obtém o ID gerado para o gasto
                print(f"Gasto salvo com ID: {self.id_gasto}")
           
            sql = "INSERT INTO gasto_grupo (id_gasto, id_grupo) VALUES (%s, %s)"
            val = (self.id_gasto, id_grupo)
            db.execute(sql, val)
            db.commit()

            # Associando o usuário ao grupo
            sql = "INSERT INTO usuario_grupo (id_user, id_grupo) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id_user=id_user"
            val = (id_user, id_grupo)
            db.execute(sql, val)
            db.commit()

            

            return True  # Operação bem-sucedida
        except Exception as e:
            db.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao salvar o gasto: {e}")
            return False  # Indica falha na operação
        finally:
            db.disconnect()


    @staticmethod
    def buscar_por_id(id_gasto: int) -> GastoResponse:
        db.connect()
        sql = "SELECT * FROM gastos WHERE id_gasto = %s"
        val = (id_gasto,)
        db.execute(sql, val)
        result = db.fetchone()
        db.disconnect()

        if result:
            gasto = GastoResponse(
                id_gasto=result[0],
                nome=result[1],
                valor=result[2],
                data=result[3].isoformat() if isinstance(result[3], datetime) else result[3]
            )
            return gasto

        return None

    @staticmethod
    def buscar_todos():
        db.connect()
        sql = "SELECT * FROM gastos"
        db.execute(sql)
        results = db.fetchall()
        db.disconnect()
        gastos = []
        for result in results:
            gasto = GastoResponse(
                id_gasto=result[0],
                nome=result[1],
                valor=result[2],
                data=result[3].isoformat() if isinstance(result[3], datetime) else str(result[3])
            )
            gastos.append(gasto)
        return gastos

    def atualizar(self):
        if self.id_gasto is not None:
            db.connect()
            sql = "UPDATE gastos SET nome = %s, valor = %s, data = %s WHERE id_gasto = %s"
            val = (self.nome, self.valor, self.data, self.id_gasto)
            db.execute(sql, val)
            db.commit()
            db.disconnect()

    @staticmethod
    def deletar_gasto(id_gasto: int) -> bool:
        db.connect()
        try:
            # Deletando o gasto da tabela principal
            sql = "DELETE FROM gastos WHERE id_gasto = %s"
            val = (id_gasto,)
            db.execute(sql, val)
            db.commit()

            if db.rowcount == 0:
                return False

            return True
        
        except Exception as e:
            db.rollback()
            print(f"Erro ao deletar o gasto: {e}")
            return False

        finally:
            db.disconnect()

   


    @staticmethod
    def remover_associacao_grupo(id_gasto: int, id_grupo: int):
        db.connect()
        sql = "DELETE FROM gasto_grupo WHERE id_gasto = %s AND id_grupo = %s"
        val = (id_gasto, id_grupo)
        db.execute(sql, val)
        db.commit()
        db.disconnect()

    @staticmethod
    def buscar_grupos_associados(id_gasto: int):
        db.connect()
        sql = """
        SELECT g.id_grupo, g.nome
        FROM grupos g
        INNER JOIN gasto_grupo gg ON g.id_grupo = gg.id_grupo
        WHERE gg.id_gasto = %s
        """
        val = (id_gasto,)
        db.execute(sql, val)
        results = db.fetchall()
        db.disconnect()
        grupos = [{"id_grupo": row[0], "nome": row[1]} for row in results]
        return grupos
    
    @staticmethod
    def buscar_por_grupo(id_grupo: int):
        db.connect()
        sql = """
        SELECT g.id_gasto, g.nome, g.valor, g.data
        FROM gastos g
        INNER JOIN gasto_grupo gg ON g.id_gasto = gg.id_gasto
        WHERE gg.id_grupo = %s
        """
        val = (id_grupo,)
        db.execute(sql, val)
        results = db.fetchall()
        db.disconnect()
        
        gastos = []
        for result in results:
            gasto = GastoResponse(
                id_gasto=result[0],
                nome=result[1],
                valor=result[2],
                data=result[3].isoformat() if isinstance(result[3], datetime) else str(result[3])
            )
            gastos.append(gasto)
        return gastos
    
    def editar(self) -> bool:
        db.connect()

        try:
            # Atualizar o gasto no banco de dados
            sql = """
            UPDATE gastos 
            SET nome = %s, valor = %s, data = %s 
            WHERE id_gasto = %s
            """
            val = (self.nome, self.valor, self.data, self.id_gasto)
            db.execute(sql, val)
            db.commit()

            return db.rowcount > 0
        
        except Exception as e:
            db.rollback()
            print(f"Erro ao editar o gasto: {e}")
            return False

        finally:
            db.disconnect()