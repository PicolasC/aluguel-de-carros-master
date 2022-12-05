
import pandas as pd
from reports.relatorios import Relatorio

from model.categoria import Categoria

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Categoria:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()    
    
        
    def inserir_categoria(self) -> Categoria:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        #Solicita ao usuario o novo código da categoria

        codigo_categoria = input("Codigo Categoria(Novo): ")
        if self.verifica_existencia_categoria(codigo_categoria):    
        
        #Solicita ao usuario a nova descrição da categoria
            descricao = input("Descrição (Novo): ")
        #Solicita ao usuario o novo valor diário
            valor_diaria = float(input("Valor diário (Novo): "))

            # Insere e persiste o novo fornecedor
            self.mongo.db["categoria"].insert_one({"codigo_categoria": codigo_categoria, "descricao": descricao, "valor_diaria": valor_diaria})

        # Recupera os dados da nova categoria criado transformando em um DataFrame
            df_categoria = self.recupera_categoria(codigo_categoria)

        # Cria um novo objeto Categoria
            nova_categoria = Categoria(df_categoria.codigo_categoria.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0])
        # Exibe os atributos da nova categoria
            print(nova_categoria.to_string())
        # Retorna o objeto nova_categoria para utilização posterior, caso necessário
            return nova_categoria
        else:
            self.mongo.close()
            print(f"O Código já {codigo_categoria} existe!")
            return None







    def atualizar_categoria(self) -> Categoria:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código da categoria a ser alterado
        codigo_categoria = (input("Código da categoria que irá alterar: "))        

        # Verifica se a categoria existe na base de dados
        if not self.verifica_existencia_categoria(codigo_categoria):

            # Solicita a nova descrição da categoria
            nova_descricao_categoria = input("Descrição (Novo): ")
            # Solicita ao usuario o novo valor diário
            novo_valor_diario = float(input("Valor diário (Novo): "))

            # Atualiza a descrição da categoria existente
            self.mongo.db["categoria"].update_one({"codigo_categoria":f"{codigo_categoria}"},{"$set": {"descricao":nova_descricao_categoria, "valor_diaria":novo_valor_diario}})            # Atualiza o valor diário existente

            # Recupera os dados da nova categoria criado transformando em um DataFrame
            df_categoria = self.recupera_categoria(codigo_categoria)

            # Cria um novo objeto Categoria
            categoria_atualizada = Categoria(df_categoria.codigo_categoria.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0])

            # Exibe os atributos da nova categoria
            print(categoria_atualizada.to_string())
            self.mongo.close()
            # Retorna a categoria_atualizada para utilização posterior, caso necessário
            return categoria_atualizada
        else:
            self.mongo.close()
            print(f"O código {codigo_categoria} não existe.")
            return None

    def excluir_categoria(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código da categoria a ser alterada
        codigo_categoria = (input("Código da Categoria que irá excluir: "))  


        # Verifica se a categoria existe na base de dados
        if not self.verifica_existencia_categoria(codigo_categoria):            
            # Recupera os dados da nova categoria criada transformando em um DataFrame
            df_categoria = self.recupera_categoria(codigo_categoria)

            opcao_excluir = input(f"Tem certeza que deseja excluir esta categoria? [S ou N]: ")
            if opcao_excluir.lower() == "s":
                self.relatorio.get_relatorio_carro()
                print("Atenção, os dados inteiros dos carro que a utilizam serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir os dados da categoria de codigo {codigo_categoria} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome a categoria da tabela
                    self.mongo.db["categoria"].delete_one({"codigo_categoria":f"{codigo_categoria}"})          
                    self.mongo.db["carro"].delete_one({"codigo_categoria":f"{codigo_categoria}"})                              
                    # Cria um novo objeto Categoria para informar que foi removido
                    categoria_excluida = Categoria(df_categoria.codigo_categoria.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0] )
                    self.mongo.close()
                    # Exibe os atributos da categoria excluída
                    print("Categoria Removida com Sucesso!")
                    print(categoria_excluida.to_string())
        else:
            self.mongo.close()
            print(f"A categoria {codigo_categoria} não existe.")






    def verifica_existencia_categoria(self, codigo_categoria:str=None, external:bool=False) -> bool:
        if external:

            self.mongo.connect()

        # Recupera os dados da nova categoria criado transformando em um DataFrame
        df_categoria = pd.DataFrame(self.mongo.db["categoria"].find({"codigo_categoria":f"{codigo_categoria}"}, {"descricao": 1, "valor_diaria": 1, "_id": 0}))
        
        if external:

            self.mongo.close()

        return df_categoria.empty





    def recupera_categoria(self, codigo_categoria:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_categoria = pd.DataFrame(list(self.mongo.db["categoria"].find({"codigo_categoria":f"{codigo_categoria}"}, {"codigo_categoria": 1, "descricao": 1, "valor_diaria": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_categoria   