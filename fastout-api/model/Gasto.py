from datetime import datetime

class Gasto:
    def __init__(self, nome, valor, data=None):
        self.id_gasto = None  # Será definido pelo banco de dados
        self.nome = nome
        self.valor = valor
        self.data = data if data else datetime.now()
        self.grupos = []  # Lista para armazenar os grupos associados

    def adicionar_grupo(self, grupo):
        if grupo not in self.grupos:
            self.grupos.append(grupo)

    def remover_grupo(self, grupo):
        if grupo in self.grupos:
            self.grupos.remove(grupo)

    def __str__(self):
        return f"Gasto(id={self.id_gasto}, nome={self.nome}, valor={self.valor}, data={self.data})"