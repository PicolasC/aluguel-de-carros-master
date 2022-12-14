from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries
import pandas as pd
from datetime import date
from reports.relatorios import Relatorio


class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()    

        
    def inserir_cliente(self) -> Cliente:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()
        

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_cliente(cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Solicita ao usuario o novo RG
            RG = input("RG (Novo): ")
            # Solicita ao usuario o novo CNH
            CNH = input("CNH (Novo): ")
            # Solicita ao usuario o novo endereco
            endereco = input("endereco (Novo): ")
            # Insere e persiste o novo cliente
            self.mongo.db["clientes"].insert_one({"cpf": cpf, "RG": RG, "CNH": CNH, "nome": nome, "endereco": endereco})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(df_cliente.cpf.values[0], df_cliente.RG.values[0], df_cliente.CNH.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            self.mongo.close()
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = int(input("CPF do cliente que deseja alterar o nome e o endereço: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpf):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Solicita o novo endereço do cliente
            novo_endereco = input("endereco (Novo): ")
            # Atualiza o nome e o endereco do cliente existente

            self.mongo.db["clientes"].update_one({"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome, "endereco": novo_endereco}})
            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)            
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(df_cliente.cpf.values[0], df_cliente.RG.values[0], df_cliente.CNH.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()


        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = int(input("CPF do Cliente que irá excluir: "))        

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpf):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)

            opcao_excluir = input(f"Tem certeza que deseja excluir este cliente? [S ou N]: ")
            if opcao_excluir.lower() == "s":
                self.relatorio.get_relatorio_alocacao()
                print("Atenção, os dados inteiros do cliente serão excluídos! incluindo as alocações nas quais ele está presente!")
                opcao_excluir = input(f"Tem certeza que deseja excluir os dados do cliente de cpf {cpf} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o cliente da tabela
                    self.mongo.db["clientes"].delete_one({"cpf":f"{cpf}"}) 
                    self.mongo.db["alocacao"].delete_one({"cpf":f"{cpf}"})                              
          
                    # Cria um novo objeto Cliente para informar que foi removido
                    cliente_excluido = Cliente(df_cliente.cpf.values[0], df_cliente.RG.values[0], df_cliente.CNH.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0])
                    self.mongo.close()
                     # Exibe os atributos do cliente excluído
                    print("Cliente Removido com Sucesso!")
                    print(cliente_excluido.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_cliente(self, cpf:str=None, external:bool=False) -> bool:
        if external:

            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

            # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(self.mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "RG": 1, "CNH": 1, "nome": 1, "endereco": 1, "_id": 0}))
        
        if external:
            
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente.empty

    def recupera_cliente(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "RG": 1, "CNH": 1, "nome": 1, "endereco": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente       