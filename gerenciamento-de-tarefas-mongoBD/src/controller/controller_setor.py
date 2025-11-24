import pandas as pd
from model.setor import Setor
from conexion.mongo_queries import MongoQueries

class Controller_Setor:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_setor(self) -> Setor:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        # Solicita ao usuario o nome do novo setor
        nome_novo_setor = input("Nome do Setor (Novo): ")

        # Lógica para Simular o Auto-Increment (Sequence) do SQL
        # Procura o maior valor de "id" na coleção "setores"
        proximo_id = self.mongo.db["setores"].aggregate([
            {
                '$group': {
                    '_id': '$setores', 
                    'proximo_id': {'$max': '$id'}
                }
            }, 
            {
                '$project': {
                    'proximo_id': {'$sum': ['$proximo_id', 1]}, 
                    '_id': 0
                }
            }
        ])

        lista_proximo = list(proximo_id)
        if lista_proximo:
            proximo_id = int(lista_proximo[0]['proximo_id'])
        else:
            # Se a coleção estiver vazia, começa do 1
            proximo_id = 1

        # Insere o documento
        self.mongo.db["setores"].insert_one({"id": proximo_id, "nome": nome_novo_setor})
        
        # Recupera os dados e cria o objeto
        df_setor = self.recupera_setor(proximo_id)
        novo_setor = Setor(df_setor.id.values[0], df_setor.nome.values[0])
        
        print(novo_setor.to_string())
        self.mongo.close()
        return novo_setor

    def atualizar_setor(self) -> Setor:
        self.mongo.connect()

        id_setor = int(input("ID do Setor que irá alterar: "))        

        if not self.verifica_existencia_setor(id_setor):
            novo_nome_setor = input("Nome do Setor (Novo): ")
            
            # Atualiza
            self.mongo.db["setores"].update_one({"id": id_setor}, {"$set": {"nome": novo_nome_setor}})
            
            df_setor = self.recupera_setor(id_setor)
            setor_atualizado = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            
            print(setor_atualizado.to_string())
            self.mongo.close()
            return setor_atualizado
        else:
            self.mongo.close()
            print(f"O ID {id_setor} não existe.")
            return None

    def excluir_setor(self):
        self.mongo.connect()

        id_setor = int(input("ID do Setor que irá excluir: "))        

        if not self.verifica_existencia_setor(id_setor):            
            df_setor = self.recupera_setor(id_setor)
            
            # Remove
            self.mongo.db["setores"].delete_one({"id": id_setor})
            
            setor_excluido = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            print("Setor Removido com Sucesso!")
            print(setor_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O ID {id_setor} não existe.")

    def verifica_existencia_setor(self, id:int=None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()
            
        df_setor = pd.DataFrame(list(self.mongo.db["setores"].find({"id": id}, {"id": 1, "nome": 1, "_id": 0})))
        
        if external:
            self.mongo.close()
            
        return df_setor.empty

    def recupera_setor(self, id:int=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()
            
        df_setor = pd.DataFrame(list(self.mongo.db["setores"].find({"id": id}, {"id": 1, "nome": 1, "_id": 0})))
        
        if external:
            self.mongo.close()
            
        return df_setor