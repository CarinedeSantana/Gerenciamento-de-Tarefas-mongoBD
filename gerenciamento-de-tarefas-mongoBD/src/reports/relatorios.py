from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_setores(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        
        # Recupera os dados transformando em um DataFrame
        # Operação equivalente a: SELECT ID, NOME FROM SETOR ORDER BY NOME
        query_result = mongo.db["setores"].find({}, 
                                                {"id": 1, 
                                                 "nome": 1, 
                                                 "_id": 0
                                                }).sort("nome", ASCENDING)
        
        df_setor = pd.DataFrame(list(query_result))
        
        # Fecha a conexão com o Mongo
        mongo.close()
        
        # Exibe o resultado
        print("\n=======================================================")
        print("              RELATÓRIO DE SETORES")
        print("=======================================================")
        # Verifica se o DataFrame não está vazio para evitar erro no print
        if not df_setor.empty:
            print(df_setor)
        else:
            print("Nenhum setor encontrado.")
            
        input("Pressione Enter para Sair do Relatório de Setores")

    def get_relatorio_funcionarios(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        
        # Pipeline de Agregação para fazer o JOIN com Setores
        # Equivalente a: SELECT f.matricula, f.nome, s.nome as setor FROM funcionarios f JOIN setores s ...
        pipeline = [
            {
                "$lookup": {
                    "from": "setores",            # Coleção a unir
                    "localField": "id_setor",     # Campo em 'funcionarios'
                    "foreignField": "id",         # Campo em 'setores'
                    "as": "setor"                 # Nome do array resultante
                }
            },
            {
                "$unwind": "$setor"               # Desenrola o array para objeto
            },
            {
                "$project": {
                    "matricula": 1,
                    "nome": 1,
                    "setor": "$setor.nome",       # Pega apenas o nome do setor
                    "_id": 0
                }
            },
            {
                "$sort": {"nome": 1}              # Ordena por nome
            }
        ]
        
        query_result = mongo.db["funcionarios"].aggregate(pipeline)
        df_funcionario = pd.DataFrame(list(query_result))
        
        mongo.close()
        
        print("\n=======================================================")
        print("            RELATÓRIO DE FUNCIONÁRIOS")
        print("=======================================================")
        if not df_funcionario.empty:
            print(df_funcionario)
        else:
            print("Nenhum funcionário encontrado.")
            
        input("Pressione Enter para Sair do Relatório de Funcionários")

    def get_relatorio_tarefas(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        
        # Pipeline para listar tarefas com o nome do responsável
        pipeline = [
            {
                "$lookup": {
                    "from": "funcionarios",
                    "localField": "matricula_funcionario",
                    "foreignField": "matricula",
                    "as": "responsavel"
                }
            },
            {
                "$unwind": "$responsavel"
            },
            {
                "$project": {
                    "id_tarefa": "$id",
                    "descricao": 1,
                    "data_limite": 1,
                    "status": 1,
                    "responsavel": "$responsavel.nome",
                    "_id": 0
                }
            },
            {
                "$sort": {"id_tarefa": 1}
            }
        ]
        
        query_result = mongo.db["tarefas"].aggregate(pipeline)
        df_tarefas = pd.DataFrame(list(query_result))
        
        mongo.close()
        
        print("\n=======================================================")
        print("           RELATÓRIO DE TODAS AS TAREFAS")
        print("=======================================================")
        if not df_tarefas.empty:
            print(df_tarefas)
        else:
            print("Nenhuma tarefa encontrada.")
            
        input("Pressione Enter para Sair do Relatório de Tarefas")

    def get_relatorio_tarefas_por_funcionario(self):
        # ATENÇÃO: Este relatório cumpre o requisito de SUMARIZAÇÃO (GROUP BY) do edital.
        # Ele conta quantas tarefas cada funcionário possui.
        
        mongo = MongoQueries()
        mongo.connect()
        
        pipeline = [
            {
                "$group": {
                    "_id": "$matricula_funcionario",  # Agrupa pela FK
                    "total_tarefas": {"$sum": 1}      # Conta as ocorrências
                }
            },
            {
                "$lookup": {
                    "from": "funcionarios",
                    "localField": "_id",              # O _id agora é a matricula (devido ao group)
                    "foreignField": "matricula",
                    "as": "func"
                }
            },
            {
                "$unwind": "$func"
            },
            {
                "$project": {
                    "funcionario": "$func.nome",
                    "matricula": "$_id",
                    "total_tarefas": 1,
                    "_id": 0
                }
            },
            {
                "$sort": {"total_tarefas": -1} # Ordena quem tem mais tarefas primeiro
            }
        ]
        
        query_result = mongo.db["tarefas"].aggregate(pipeline)
        df_agrupado = pd.DataFrame(list(query_result))
        
        mongo.close()
        
        print("\n=======================================================")
        print("      RELATÓRIO: QUANTIDADE DE TAREFAS POR FUNCIONÁRIO")
        print("=======================================================")
        if not df_agrupado.empty:
            print(df_agrupado)
        else:
            print("Nenhum dado encontrado.")
            
        input("Pressione Enter para Sair do Relatório de Tarefas por Funcionário")