from model.alocacao import Alocacao
from model.clientes import Cliente
from controller.controller_cliente import Controller_Cliente
from model.carros import Carro
from controller.controller_carro import Controller_Carro
from datetime import date
from conexion.oracle_queries import OracleQueries
from conexion.mongo_queries import MongoQueries
from reports.relatorios import Relatorio
import pandas as pd
from datetime import datetime

class Controller_Alocacao:
    def __init__(self):
        self.mongo = MongoQueries()
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_carro = Controller_Carro()
        self.relatorio = Relatorio()
        
    def inserir_alocacao(self) -> Alocacao:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        self.mongo.connect()
        

        # Lista os clientes existentes para inserir na alocaaco
        self.relatorio.get_relatorio_clientes()
        cpf = str(input("Digite o número do CPF do Cliente: "))
        cliente = self.valida_cliente(cpf)
        if cliente == None:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")
            return None

        # Lista os carros existentes para inserir na alocacao
        self.relatorio.get_relatorio_carro()
        chassi = str(input("Digite o número do chassi do carro: "))
        carro = self.valida_carro(chassi)
        if carro == None:
            self.mongo.close()
            print(f"O carro {chassi} não existe.")
            return None
       
        data_saida = datetime.today().strftime("%m-%d-%y")
        

        # Passar o código de alocação
        codigo_alocacao = str(input("Digite o codigo de alocação "))

        if self.verifica_existencia_alocacao(codigo_alocacao):               


        # Passar a data obrigatória de entrega
            data_entrega = str(input("Digite a data de entrega mm-dd-aaaa "))


        # Insere e persiste o novo carro
            self.mongo.db["alocacao"].insert_one({"codigo_alocacao": codigo_alocacao, "cpf": cpf, "chassi": chassi, "data_saida": data_saida, "data_entrega": data_entrega})

        # Recupera os dados da nova alocacao criada transformando-a em um DataFrame
            df_alocacao = self.recupera_alocacao(codigo_alocacao)        

        # Cria um novo objeto Alocacao
            novo_alocacao = Alocacao(df_alocacao.codigo_alocacao.values[0], df_alocacao.data_entrega.values[0], df_alocacao.data_saida.values[0], carro, cliente)

            print(novo_alocacao.to_string())
            self.mongo.close()
            # Retorna o objeto nova_alocacao para utilização posterior, caso necessário
            return novo_alocacao
        else:
            self.mongo.close()
            print(f"O Código já {codigo_alocacao} existe!")
            return None


    def atualizar_alocacao(self) -> Alocacao:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o codigo cuja alocação será alterada
        codigo_alocacao = str(input("Digite o codigo de alocação das informações que serão alteradas: "))

    
        # Verifica se a alocação existe na base de dados
        if not self.verifica_existencia_alocacao(codigo_alocacao):


            # Inserir a nova data de entrega
            data_entrega = str(input("Digite a nova data de entrega mm-dd-aaaa: "))


            # Lista os clientes existentes para inserir na alocação
            self.relatorio.get_relatorio_clientes()
            cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(cpf)
            if cliente == None:
                self.mongo.close()
                return None

            # Lista os carros existentes para inserir na alocação
            self.relatorio.get_relatorio_carro()
            chassi = str(input("Digite o número do chassi do carro: "))
            carro = self.valida_carro(chassi)
            if carro == None:
                self.mongo.close()
                return None

            data_saida = datetime.today().strftime("%m-%d-%y")


            # Atualiza a descrição da alocação presente
            self.mongo.db["alocacao"].update_one({"codigo_alocacao":f"{codigo_alocacao}"},{"$set": {"codigo_alocacao":codigo_alocacao, "cpf":cpf, "chassi":chassi, "data_saida":data_saida, "data_entrega":data_entrega}})            # Recupera os dados da nova alocacao criado transformando em um DataFrame
            df_alocacao = self.recupera_alocacao(codigo_alocacao)
            # Cria um novo objeto Alocacao
            alocacao_atualizada = Alocacao(df_alocacao.data_entrega.values[0],df_alocacao.data_entrega.values[0], df_alocacao.data_saida.values[0], cpf, chassi)
            # Exibe os atributos da nova alocação
            print(alocacao_atualizada.to_string())
            # Retorna o objeto alocacao_atualizada para utilização posterior, caso necessário
            return alocacao_atualizada
        else:
            print(f"O codigo de alocacao {codigo_alocacao} não existe.")
            self.mongo.close()
            return None

    def excluir_alocacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o codigo cuja alocação será alterada
        codigo_alocacao = str(input("Digite o codigo de alocação das informações que serão apagadas: "))

       
     

        # Verifica se a alocação existe na base de dados
        if not self.verifica_existencia_alocacao(codigo_alocacao):               
            
            # Recupera os dados da nova alocação criada transformando em um DataFrame
            df_alocacao = self.recupera_alocacao(codigo_alocacao)
            cliente = self.valida_cliente(df_alocacao.cpf.values[0])
            carro = self.valida_carro(df_alocacao.chassi.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir esta alocação? [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso a alocacao inteira inteira será excluída!")
                opcao_excluir = input(f"Tem certeza que deseja excluir a alocação do código {codigo_alocacao} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome a alocação da tabela
                    self.mongo.db["alocacao"].delete_one({"codigo_alocacao":f"{codigo_alocacao}"})
                    print("Alocação removida com sucesso!")
                    # Cria um novo objeto alocacao para informar que foi removida
                    alocacao_excluida = Alocacao(df_alocacao.data_entrega.values[0], df_alocacao.data_saida.values[0], cliente, carro)
                    self.mongo.close()
                    # Exibe os atributos da alocacao excluída
                    print("Alocação Removida com Sucesso!")
                    print(alocacao_excluida.to_string())
        else:
            self.mongo.close()
            print(f"Não existe uma alocação de código {codigo_alocacao}.")


    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.cpf
                    , c.rg 
                    , c.cnh
                    , c.nome 
                    , c.endereco 
                from clientes c
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_carros(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select car.chassi
                    , car.cor
                    , car.modelo
                    , car.marca
                    , car.placa
                    , car.ano

                from carro car
                order by car.chassi
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))


    def verifica_existencia_alocacao(self, codigo_alocacao:str=None, external:bool= False) -> bool:
        if external:
            self.mongo.connect()

        # Recupera os dados do novo carro criado transformando em um DataFrame
        df_alocacao = pd.DataFrame(self.mongo.db["alocacao"].find({"codigo_alocacao":f"{codigo_alocacao}"}, {"codigo_alocacao": 1,"cpf": 1,"chassi": 1,"data_saida": 1, "data_entrega": 1, "_id": 0}))

        if external:
            self.mongo.close()
        return df_alocacao.empty

    def recupera_alocacao(self, codigo_alocacao:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_alocacao = pd.DataFrame(list(self.mongo.db["alocacao"].find({"codigo_alocacao":f"{codigo_alocacao}"}, {"codigo_alocacao": 1,"cpf": 1,"chassi": 1,"data_saida": 1, "data_entrega": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_alocacao




    def valida_cliente(self, cpf:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(cpf = cpf, external = True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.ctrl_cliente.recupera_cliente(cpf=cpf, external= True)
            
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpf.values[0], df_cliente.RG.values[0], df_cliente.CNH.values[0], df_cliente.endereco.values[0], df_cliente.nome.values[0])
            return cliente

    def valida_carro(self, chassi:str=None) -> Carro:
        if self.ctrl_carro.verifica_existencia_carro(chassi = chassi, external = True):
            print(f"O Chassi {chassi} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = self.ctrl_carro.recupera_carro(chassi = chassi, external= True)
            # Cria um novo objeto Carro
            carro = Carro(df_carro.chassi.values[0], df_carro.cor.values[0], df_carro.modelo.values[0],  df_carro.marca.values[0], df_carro.placa.values[0], df_carro.ano.values[0], df_carro.codigo_categoria.values[0])
            return carro