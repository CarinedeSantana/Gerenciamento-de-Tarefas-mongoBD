import pymongo
from pymongo import MongoClient
from pandas import DataFrame
import json
import os

class MongoQueries:
    def __init__(self):
        self.host = "localhost"
        self.port = 27017
        self.service_name = 'labdatabase'

        # --- CORREÇÃO DE CAMINHO DO ARQUIVO DE SENHA ---
        # Pega o diretório onde este arquivo (mongo_queries.py) está localizado
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Monta o caminho para: src/conexion/passphrase/authentication.mongo
        # Se sua pasta se chamar "senhas", altere "passphrase" para "senhas" abaixo
        file_path = os.path.join(base_path, "passphrase", "authentication.mongo")

        # Verifica se o arquivo existe antes de tentar abrir
        if not os.path.exists(file_path):
            # Tenta procurar na raiz src/passphrase se não achar em src/conexion/passphrase
            file_path = os.path.join(base_path, "..", "passphrase", "authentication.mongo")
            
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.user, self.passwd = f.read().strip().split(',')
        else:
            print(f"Atenção: Arquivo de autenticação não encontrado em: {file_path}")
            self.user, self.passwd = None, None

    def __del__(self):
        if hasattr(self, "mongo_client"):
            self.close()

    def connect(self):
        '''
        Realiza a conexão com o MongoDB utilizando as credenciais fornecidas.
        Return: O objeto de banco de dados para realizar operações.
        '''
        # Conexão formatada para incluir autenticação se houver senha definida
        if self.user and self.passwd:
            # Ajuste para codificar caracteres especiais na senha se necessário
            self.mongo_client = MongoClient(f"mongodb://{self.user}:{self.passwd}@localhost:27017/")
        else:
            self.mongo_client = MongoClient("mongodb://localhost:27017/")
            
        self.db = self.mongo_client["labdatabase"]
        return self.db

    def close(self):
        '''
        Fecha a conexão com o cliente MongoDB.
        '''
        if hasattr(self, "mongo_client"):
            self.mongo_client.close()

    # --- Métodos equivalentes ao sqlToDataFrame e sqlToMatrix ---

    def execute_query(self, collection_name: str, query: dict = None, projection: dict = None) -> DataFrame:
        '''
        Executa uma consulta (find) no MongoDB e retorna um DataFrame.
        Equivalente ao sqlToDataFrame do Oracle.
        '''
        if query is None:
            query = {}
        
        if self.connect():
            collection = self.db[collection_name]
            cursor = collection.find(query, projection)
            lista_documentos = list(cursor)
            self.close()
            return DataFrame(lista_documentos)
        return DataFrame()

    def execute_aggregation(self, collection_name: str, pipeline: list) -> DataFrame:
        '''
        Executa uma agregação (pipeline) no MongoDB. 
        Essencial para os relatórios solicitados no Edital.
        '''
        if self.connect():
            collection = self.db[collection_name]
            cursor = collection.aggregate(pipeline)
            lista_documentos = list(cursor)
            self.close()
            return DataFrame(lista_documentos)
        return DataFrame()

    # --- Métodos equivalentes ao write (INSERT, UPDATE, DELETE) ---

    def execute_insert(self, collection_name: str, document: dict):
        '''Insere um documento em uma coleção.'''
        if self.connect():
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            # self.close() # Opcional fechar aqui ou deixar o controller gerenciar
            return result

    def execute_update(self, collection_name: str, query: dict, new_values: dict):
        '''Atualiza um documento.'''
        if self.connect():
            collection = self.db[collection_name]
            if not any(key.startswith('$') for key in new_values):
                update_cmd = {"$set": new_values}
            else:
                update_cmd = new_values
            collection.update_one(query, update_cmd)
            # self.close()

    def execute_delete(self, collection_name: str, query: dict):
        '''Remove um documento.'''
        if self.connect():
            collection = self.db[collection_name]
            collection.delete_one(query)
            # self.close()