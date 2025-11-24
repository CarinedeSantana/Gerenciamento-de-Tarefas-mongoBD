from datetime import date
from model.funcionario import Funcionario 

class Tarefa:
    def __init__(self, 
                 id:int=None,
                 descricao:str=None,
                 data_limite:date=None,
                 status:str=None,
                 funcionario:Funcionario=None # Objeto Funcionario para a relação FK
                 ):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_data_limite(data_limite)
        self.set_status(status)
        self.set_funcionario(funcionario)

    def set_id(self, id:int):
        self.id = id

    def set_descricao(self, descricao:str):
        self.descricao = descricao

    def set_data_limite(self, data_limite:date):
        self.data_limite = data_limite

    def set_status(self, status:str):
        self.status = status
    
    def set_funcionario(self, funcionario:Funcionario):
        self.funcionario = funcionario

    def get_id(self) -> int:
        return self.id

    def get_descricao(self) -> str:
        return self.descricao

    def get_data_limite(self) -> date:
        return self.data_limite
    
    def get_status(self) -> str:
        return self.status

    def get_funcionario(self) -> Funcionario:
        return self.funcionario

    def to_string(self):
        # Inclui o nome do funcionário na string
        nome_funcionario = self.get_funcionario().get_nome() if self.get_funcionario() else "N/A"
        return f"Tarefa ID: {self.get_id()} | Descrição: {self.get_descricao()} | Data Limite: {self.get_data_limite()} | Status: {self.get_status()} | Funcionário: {nome_funcionario}"
