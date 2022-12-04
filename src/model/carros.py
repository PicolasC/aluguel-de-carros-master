from model.categoria import Categoria

class Carro:
    def __init__(self, 
                 chassi:str=None, 
                 cor:str=None, 
                 modelo:str=None,
                 marca:str=None,
                 placa:str=None, 
                 ano:int=None, 

                 codigo_categoria:Categoria=None 

                 ):
        self.set_chassi(chassi)
        self.set_cor(cor)
        self.set_modelo(modelo) 
        self.set_marca(marca)
        self.set_placa(placa)
        self.set_ano(ano)


        self.set_codigo_categoria(codigo_categoria)


    def set_chassi(self, chassi:str):
        self.chassi = chassi

    def set_cor(self, cor:str):
        self.cor = cor

    def set_modelo(self, modelo:str):
        self.modelo = modelo

    def set_marca(self, marca:str):
        self.marca = marca

    def set_placa(self, placa:str):
        self.placa = placa

    def set_ano(self, ano:int):
        self.ano = ano

    def set_codigo_categoria(self, codigo_categoria:Categoria):
        self.codigo_categoria = codigo_categoria








    def get_chassi(self) -> str:
        return self.chassi

    def get_cor(self) -> str:
        return self.cor

    def get_modelo(self) -> str:
        return self.modelo

    def get_marca(self) -> str:
        return self.marca

    def get_placa(self) -> str:
        return self.placa

    def get_ano(self) -> int:
        return self.ano



    def get_codigo_categoria(self) -> Categoria:
        return self.codigo_categoria




    def to_string(self) -> str:
        return f"Chassi: {self.get_chassi()} | Cor: {self.get_cor()} | Modelo: {self.get_modelo()}| Marca: {self.get_marca()} | Placa: {self.get_placa()} | Ano: {self.get_ano()} | Codigo Categoria: {self.get_codigo_categoria()}"