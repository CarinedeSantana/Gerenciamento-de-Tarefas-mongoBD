from conexion.mongo_queries import MongoQueries
from datetime import datetime

def create_collections(mongo: MongoQueries):
    # Lista de coleções para limpar antes de inserir os dados novos
    collections = ["setores", "funcionarios", "tarefas"]
    
    for col in collections:
        mongo.db[col].drop()
        print(f"Coleção '{col}' apagada (DROP).")
        # No Mongo, a coleção é criada automaticamente na primeira inserção,
        # mas podemos criar explicitamente se quisermos validações (opcional).

def generate_records(mongo: MongoQueries):
    # --- 1. Inserindo SETORES ---
    setores = [
        {"id": 1, "nome": "Desenvolvimento"},
        {"id": 2, "nome": "Recursos Humanos"},
        {"id": 3, "nome": "Financeiro"}
    ]
    mongo.db["setores"].insert_many(setores)
    print(f"Inseridos {len(setores)} registros em 'setores'.")

    # --- 2. Inserindo FUNCIONÁRIOS ---
    # Note que usamos o ID do setor para fazer o vínculo (Relacionamento)
    funcionarios = [
        {"matricula": "F001", "nome": "Ana Silva", "id_setor": 1},
        {"matricula": "F002", "nome": "Carlos Souza", "id_setor": 1},
        {"matricula": "F003", "nome": "Beatriz Costa", "id_setor": 2},
        {"matricula": "F004", "nome": "Daniel Oliveira", "id_setor": 3}
    ]
    mongo.db["funcionarios"].insert_many(funcionarios)
    print(f"Inseridos {len(funcionarios)} registros em 'funcionarios'.")

    # --- 3. Inserindo TAREFAS ---
    # Usamos objetos datetime para as datas
    tarefas = [
        {
            "id": 1, 
            "descricao": "Implementar Login", 
            "data_limite": datetime(2023, 12, 20), 
            "status": "Em Andamento", 
            "matricula_funcionario": "F001"
        },
        {
            "id": 2, 
            "descricao": "Recrutar Dev Senior", 
            "data_limite": datetime(2023, 11, 30), 
            "status": "Pendente", 
            "matricula_funcionario": "F003"
        },
        {
            "id": 3, 
            "descricao": "Fechar Balanço Mensal", 
            "data_limite": datetime(2023, 12, 5), 
            "status": "Concluída", 
            "matricula_funcionario": "F004"
        },
        {
            "id": 4, 
            "descricao": "Corrigir Bug na API", 
            "data_limite": datetime(2023, 12, 21), 
            "status": "Pendente", 
            "matricula_funcionario": "F002"
        }
    ]
    mongo.db["tarefas"].insert_many(tarefas)
    print(f"Inseridos {len(tarefas)} registros em 'tarefas'.")

def run():
    mongo = MongoQueries()
    mongo.connect()

    print("Iniciando carga de dados no MongoDB...")
    
    # 1. Limpa o banco (Drop collections)
    create_collections(mongo)
    
    # 2. Insere os dados iniciais (Seed)
    generate_records(mongo)
    
    mongo.close()
    print("Carga de dados finalizada com sucesso!")

if __name__ == '__main__':
    run()