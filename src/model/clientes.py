from datetime import date

class Cliente:
    def __init__(self, 
                 CPF:str=None, 
                 RG:str=None,
                 CNH:str=None,
                 nome:str=None,
                 endereco:str=None
                ):
        self.set_CPF(CPF)
        self.set_nome(nome)
        self.set_RG(RG)
        self.set_CNH(CNH)
        self.set_endereco(endereco)

    def set_CPF(self, CPF:str):
        self.CPF = CPF

    def set_nome(self, nome:str):
        self.nome = nome

    def set_RG(self, RG:str):
        self.RG = RG

    def set_CNH(self, CNH:str):
        self.CNH = CNH

    def set_endereco(self, endereco:str):
        self.endereco = endereco

    def get_CPF(self) -> str:
        return self.CPF

    def get_nome(self) -> str:
        return self.nome

    def get_RG(self) -> str:
        return self.RG

    def get_CNH(self) -> str:
        return self.CNH

    def get_endereco(self) -> str:
        return self.endereco


    def to_string(self) -> str:
        return f"CPF: {self.get_CPF()} | Nome: {self.get_nome()} | RG: {self.get_RG()} | CNH: {self.get_CNH()} | Endereco: {self.get_endereco()} "