class Setor:
    def __init__(self, 
                 id:int=None, 
                 nome:str=None
                 ):
        self.set_id(id)
        self.set_nome(nome)

    def set_id(self, id:int):
        self.id = id

    def set_nome(self, nome:str):
        self.nome = nome

    def get_id(self) -> int:
        return self.id

    def get_nome(self) -> str:
        return self.nome

    def to_string(self) -> str:
        return f"ID Setor: {self.get_id()} | Nome: {self.get_nome()}"