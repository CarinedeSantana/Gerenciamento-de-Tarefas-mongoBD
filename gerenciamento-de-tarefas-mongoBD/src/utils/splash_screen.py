from conexion.mongo_queries import MongoQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # No MongoDB, não precisamos pré-definir query strings SQL no init.
        # A contagem é feita diretamente nos métodos abaixo.
        
        # Nome(s) do(s) criador(es)
        self.created_by = "Carine, Gustavo, Juan, Luisa, Victor" 
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

    def get_total_setores(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Retorna o total de documentos na coleção 'setores'
        total = mongo.db["setores"].count_documents({})
        mongo.close()
        return total

    def get_total_funcionarios(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Retorna o total de documentos na coleção 'funcionarios'
        total = mongo.db["funcionarios"].count_documents({})
        mongo.close()
        return total

    def get_total_tarefas(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Retorna o total de documentos na coleção 'tarefas'
        total = mongo.db["tarefas"].count_documents({})
        mongo.close()
        return total

    def get_updated_screen(self):
        return f"""
        ########################################################
        #             SISTEMA DE GESTÃO DE TAREFAS              
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - SETORES:          {str(self.get_total_setores()).rjust(5)}
        #      2 - FUNCIONÁRIOS:     {str(self.get_total_funcionarios()).rjust(5)}
        #      3 - TAREFAS:          {str(self.get_total_tarefas()).rjust(5)}
        #
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """