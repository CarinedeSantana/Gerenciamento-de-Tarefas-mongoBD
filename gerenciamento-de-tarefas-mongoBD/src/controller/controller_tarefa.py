import pandas as pd
from model.tarefa import Tarefa
from model.funcionario import Funcionario
from model.setor import Setor
from controller.controller_funcionario import Controller_Funcionario
from controller.controller_setor import Controller_Setor
from conexion.mongo_queries import MongoQueries
from datetime import datetime
from dateutil import parser 

class Controller_Tarefa:
    def __init__(self):
        self.ctrl_funcionario = Controller_Funcionario()
        self.ctrl_setor = Controller_Setor() 
        self.mongo = MongoQueries()
        
    def inserir_tarefa(self) -> Tarefa:
        self.mongo.connect()
        
        # self.listar_funcionarios() # Implementar se necessário
        matricula_funcionario = input("Digite a Matrícula do Funcionário (Responsável): ")
        funcionario = self.valida_funcionario(matricula_funcionario)
        if funcionario == None:
            self.mongo.close()
            return None

        descricao = input("Descrição da Tarefa: ")
        status = input("Status da Tarefa (Ex: Pendente, Em Andamento, Concluída): ")
        
        # Tratamento de Data
        data_limite_str = input("Data Limite (formato DD/MM/AAAA): ")
        try:
            data_limite = parser.parse(data_limite_str, dayfirst=True)
            # Formata para string ou salva como datetime, depende da preferência. 
            # Mongo aceita datetime nativo. Aqui vou converter para string formato ISO para ficar legível no JSON, 
            # ou manter datetime se preferir querys de data. O exemplo do professor usava string em alguns pontos.
            # Vou manter como string dd/mm/yyyy para visualização simples ou objeto datetime.
            # Vamos salvar o objeto datetime para facilitar sorting se necessário.
        except:
            print("Formato de data inválido.")
            self.mongo.close()
            return None

        # Auto-Increment ID da Tarefa
        proximo_id = self.mongo.db["tarefas"].aggregate([
            {
                '$group': {
                    '_id': '$tarefas', 
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
            proximo_id = 1

        data = dict(
            id=proximo_id, 
            descricao=descricao, 
            data_limite=data_limite, # Salvando como Date Object do Python
            status=status, 
            matricula_funcionario=funcionario.get_matricula()
        )

        self.mongo.db["tarefas"].insert_one(data)
        
        df_tarefa = self.recupera_tarefa(proximo_id)
        nova_tarefa = Tarefa(df_tarefa.id.values[0], df_tarefa.descricao.values[0], df_tarefa.data_limite.values[0], df_tarefa.status.values[0], funcionario)
        
        print(nova_tarefa.to_string())
        self.mongo.close()
        return nova_tarefa

    def atualizar_tarefa(self) -> Tarefa:
        self.mongo.connect()

        id_tarefa = int(input("ID da Tarefa que irá alterar: "))        

        if not self.verifica_existencia_tarefa(id_tarefa):
            
            matricula_funcionario = input("Nova Matrícula do Funcionário (Responsável): ")
            funcionario = self.valida_funcionario(matricula_funcionario)
            if funcionario == None:
                self.mongo.close()
                return None

            nova_descricao = input("Nova Descrição da Tarefa: ")
            novo_status = input("Novo Status da Tarefa: ")
            nova_data_limite_str = input("Nova Data Limite (formato DD/MM/AAAA): ")
            try:
                nova_data_limite = parser.parse(nova_data_limite_str, dayfirst=True)
            except:
                print("Data inválida")
                self.mongo.close()
                return None

            self.mongo.db["tarefas"].update_one(
                {"id": id_tarefa},
                {"$set": {
                    "descricao": nova_descricao,
                    "status": novo_status,
                    "data_limite": nova_data_limite,
                    "matricula_funcionario": funcionario.get_matricula()
                }}
            )
            
            df_tarefa = self.recupera_tarefa(id_tarefa)
            tarefa_atualizada = Tarefa(df_tarefa.id.values[0], df_tarefa.descricao.values[0], df_tarefa.data_limite.values[0], df_tarefa.status.values[0], funcionario)
            
            print(tarefa_atualizada.to_string())
            self.mongo.close()
            return tarefa_atualizada
        else:
            print(f"O ID {id_tarefa} não existe.")
            self.mongo.close()
            return None

    def excluir_tarefa(self):
        self.mongo.connect()

        id_tarefa = int(input("ID da Tarefa que irá excluir: "))        

        if not self.verifica_existencia_tarefa(id_tarefa):            
            df_tarefa = self.recupera_tarefa(id_tarefa)
            funcionario = self.valida_funcionario(df_tarefa.matricula_funcionario.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir a tarefa {id_tarefa} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                self.mongo.db["tarefas"].delete_one({"id": id_tarefa})
                
                tarefa_excluida = Tarefa(df_tarefa.id.values[0], df_tarefa.descricao.values[0], df_tarefa.data_limite.values[0], df_tarefa.status.values[0], funcionario)
                print("Tarefa Removida com Sucesso!")
                print(tarefa_excluida.to_string())
            self.mongo.close()
        else:
            print(f"O ID {id_tarefa} não existe.")
            self.mongo.close()

    def verifica_existencia_tarefa(self, id:int=None) -> bool:
        df_tarefa = pd.DataFrame(list(self.mongo.db["tarefas"].find({"id": id}, {"id": 1, "_id": 0})))
        return df_tarefa.empty

    def recupera_tarefa(self, id:int=None) -> pd.DataFrame:
        df_tarefa = pd.DataFrame(list(self.mongo.db["tarefas"].find({"id": id}, {"id": 1, "descricao": 1, "data_limite": 1, "status": 1, "matricula_funcionario": 1, "_id": 0})))
        return df_tarefa

    def valida_funcionario(self, matricula_funcionario:str=None) -> Funcionario:
        if self.ctrl_funcionario.verifica_existencia_funcionario(matricula_funcionario, external=True):
            print(f"A Matrícula {matricula_funcionario} informada não existe na base.")
            return None
        else:
            df_funcionario = self.ctrl_funcionario.recupera_funcionario(matricula_funcionario, external=True)
            
            # Precisa recuperar o Setor também para montar o objeto Funcionario completo
            id_setor = int(df_funcionario.id_setor.values[0])
            df_setor = self.ctrl_setor.recupera_setor(id_setor, external=True)
            setor = Setor(df_setor.id.values[0], df_setor.nome.values[0])
            
            funcionario = Funcionario(df_funcionario.matricula.values[0], df_funcionario.nome.values[0], setor)
            return funcionario