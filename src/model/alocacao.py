from datetime import date
from model.carros import Carro
from model.clientes import Cliente

class Alocacao:
    def __init__(self, 
                 codigo:str=None, 

                 data_entrega:str=None,

                 data_saida:date=None,

                 cpf:Cliente=None,
                 chassi:Carro=None

                 ):
        self.set_codigo(codigo)
        self.set_data_entrega(data_entrega)
        self.set_data_saida(data_saida)
        self.set_cpf(cpf)
        self.set_chassi(chassi)

    def set_codigo(self, codigo:str):
        self.codigo = codigo

    def set_data_entrega(self, data_entrega:str):
        self.data_entrega = data_entrega

    def set_data_saida(self, data_saida:date):
        self.data_saida = data_saida

    
    def set_cpf(self, cpf:Cliente):
        self.cpf = cpf

    def set_chassi(self, chassi:Carro):
        self.chassi = chassi

    def get_codigo(self) -> str:
        return self.codigo

    def get_data_entrega(self) -> str:
        return self.data_entrega

    def get_data_saida(self) -> date:
        return self.data_saida
    
    def get_cpf(self) -> Cliente:
        return self.cpf

    def get_chassi(self) -> Carro:
        return self.chassi

    def to_string(self) -> str:
        return f"Codigo: {self.get_codigo()} |Data de entrega: {self.get_data_entrega()} | Data de saída: {self.get_data_saida()} | Chassi do carro: {self.get_chassi()} | CPF do cliente: {self.get_cpf()}"