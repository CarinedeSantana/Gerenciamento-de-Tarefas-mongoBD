import pandas as pd
from model.funcionario import Funcionario
from model.setor import Setor
from controller.controller_setor import Controller_Setor
from conexion.mongo_queries import MongoQueries

class Controller_Funcionario:
    def __init__(self):
        self.ctrl_setor = Controller_Setor()
        self.mongo = MongoQueries()
        
    def inserir_funcionario(self) -> Funcionario:
        self.mongo.connect()
        
        # Lista setores (Implementar listagem se necessário ou usar relatório)
        # self.listar_setores() 
        
        id_setor = int(input("Digite o ID do Setor (Existente): "))
        setor = self.valida_setor(id_setor)
        if setor == None:
            self.mongo.close()
            return None

        matricula_funcionario = input("Matrícula do Funcionário (Nova): ")
        
        # Verifica se já existe (lógica inversa do empty: se não estiver vazio, existe)
        if not self.verifica_existencia_funcionario(matricula_funcionario):
            print(f"A Matrícula {matricula_funcionario} já existe.")
            self.mongo.close()
            return None

        nome_funcionario = input("Nome do Funcionário (Novo): ")

        # Insere no MongoDB
        self.mongo.db["funcionarios"].insert_one({
            "matricula": matricula_funcionario,
            "nome": nome_funcionario,
            "id_setor": int(setor.get_id())
        })
        
        df_funcionario = self.recupera_funcionario(matricula_funcionario)
        novo_funcionario = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
        
        print(novo_funcionario.to_string())
        self.mongo.close()
        return novo_funcionario

    def atualizar_funcionario(self) -> Funcionario:
        self.mongo.connect()

        matricula_funcionario = input("Matrícula do Funcionário que deseja atualizar: ") 

        if self.verifica_existencia_funcionario(matricula_funcionario): 
            print(f"A Matrícula {matricula_funcionario} não existe.")
            self.mongo.close()
            return None
        
        id_setor = int(input("Novo ID do Setor (Existente): "))
        setor = self.valida_setor(id_setor)
        if setor == None:
            self.mongo.close()
            return None
        
        novo_nome = input("Nome do Funcionário (Novo): ")

        # Atualiza
        self.mongo.db["funcionarios"].update_one(
            {"matricula": matricula_funcionario},
            {"$set": {"nome": novo_nome, "id_setor": int(setor.get_id())}}
        )
        
        df_funcionario = self.recupera_funcionario(matricula_funcionario)
        funcionario_atualizado = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
        
        print(funcionario_atualizado.to_string())
        self.mongo.close()
        return funcionario_atualizado

    def excluir_funcionario(self):
        self.mongo.connect()

        matricula_funcionario = input("Matrícula do Funcionário que irá excluir: ") 

        if self.verifica_existencia_funcionario(matricula_funcionario): 
            print(f"A Matrícula {matricula_funcionario} não existe.")
            self.mongo.close()
            return None
            
        df_funcionario = self.recupera_funcionario(matricula_funcionario)
        setor = self.valida_setor(int(df_funcionario.id_setor.values[0]))
        
        self.mongo.db["funcionarios"].delete_one({"matricula": matricula_funcionario})
        
        funcionario_excluido = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
        print("Funcionário Removido com Sucesso!")
        print(funcionario_excluido.to_string())
        self.mongo.close()

    def verifica_existencia_funcionario(self, matricula:str=None, external:bool=False) -> bool: 
        if external:
            self.mongo.connect()
        
        df_funcionario = pd.DataFrame(list(self.mongo.db["funcionarios"].find({"matricula": matricula}, {"matricula": 1, "nome": 1, "id_setor": 1, "_id": 0})))
        
        if external:
            self.mongo.close()
            
        return df_funcionario.empty
    
    def recupera_funcionario(self, matricula:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()
            
        df_funcionario = pd.DataFrame(list(self.mongo.db["funcionarios"].find({"matricula": matricula}, {"matricula": 1, "nome": 1, "id_setor": 1, "_id": 0})))
        
        if external:
            self.mongo.close()
            
        return df_funcionario

    def valida_setor(self, id_setor:int=None) -> Setor:
        # Utiliza external=True para não fechar a conexão do controller principal
        if self.ctrl_setor.verifica_existencia_setor(id_setor, external=True):
            print(f"O ID do Setor {id_setor} informado não existe na base.")
            return None
        else:
            df_setor = self.ctrl_setor.recupera_setor(id_setor, external=True)
            setor = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            return setor