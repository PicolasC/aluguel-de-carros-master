from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_pedidos_e_itens(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db.pedidos.aggregate([{
                                                    "$lookup":{"from":"itens_pedido",
                                                               "localField":"codigo_pedido",
                                                               "foreignField":"codigo_pedido",
                                                               "as":"item"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": { "path": "$item"}
                                                   },
                                                   {
                                                    "$lookup":{"from":"clientes",
                                                               "localField":"cpf",
                                                               "foreignField":"cpf",
                                                               "as":"cliente"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": { "path": "$cliente" }
                                                   },
                                                   {
                                                    "$lookup":{"from":"fornecedores",
                                                               "localField":"cnpj",
                                                               "foreignField":"cnpj",
                                                               "as":"fornecedor"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": {"path": "$fornecedor"}
                                                   },
                                                   {
                                                    "$lookup":{"from":'produtos',
                                                               "localField":"item.codigo_produto",
                                                               "foreignField":"codigo_produto",
                                                               "as":"produto"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": {"path": "$produto"}
                                                   },
                                                   {
                                                    "$project": {"codigo_pedido": 1,
                                                                 "codigo_item_pedido": "$item.codigo_item_pedido",
                                                                 "cliente": "$cliente.nome",
                                                                 "data_pedido":1,
                                                                 "fornecedor": "$fornecedor.razao_social",
                                                                 "produto": "$produto.descricao_produto",
                                                                 "quantidade": "$item.quantidade",
                                                                 "valor_unitario": "$item.valor_unitario",
                                                                 "valor_total": {'$multiply':['$item.quantidade','$item.valor_unitario']},
                                                                 "_id": 0
                                                                }
                                                   }])
        
        df_pedidos_itens = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_pedidos_itens)
        input("Pressione Enter para Sair do Relatório de Pedidos")

    def get_relatorio_pedidos_por_fornecedor(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pedidos"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$cnpj', 
                                                            'qtd_pedidos': {
                                                                '$sum': 1
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': '$_id', 
                                                            'qtd_pedidos': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'pedidos', 
                                                            'localField': 'cnpj', 
                                                            'foreignField': 'cnpj', 
                                                            'as': 'pedido'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$pedido'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': 1, 
                                                            'qtd_pedidos': 1, 
                                                            'pedido': '$pedido.codigo_pedido', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'itens_pedido', 
                                                            'localField': 'pedido', 
                                                            'foreignField': 'codigo_pedido', 
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': 1, 
                                                            'qtd_pedidos': 1, 
                                                            'quantidade': '$item.quantidade', 
                                                            'valor_unitario': '$item.valor_unitario', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$group': {
                                                            '_id': {
                                                                'cnpj': '$cnpj', 
                                                                'qtd_pedidos': '$qtd_pedidos'
                                                            }, 
                                                            'valor_total': {
                                                                '$sum': {
                                                                    '$multiply': [
                                                                        '$quantidade', '$valor_unitario'
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$_id'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': '$_id.cnpj', 
                                                            'qtd_pedidos': '$_id.qtd_pedidos', 
                                                            'valor_total': '$valor_total', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'fornecedores', 
                                                            'localField': 'cnpj', 
                                                            'foreignField': 'cnpj', 
                                                            'as': 'fornecedor'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$fornecedor'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'empresa': '$fornecedor.nome_fantasia', 
                                                            'qtd_pedidos': 1, 
                                                            'valor_total': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'empresa': 1
                                                        }
                                                    }
                                                ])
        df_pedidos_fornecedor = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_pedidos_fornecedor[["empresa", "qtd_pedidos", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Fornecedores")

    def get_relatorio_produtos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["produtos"].find({}, 
                                                 {"codigo_produto": 1, 
                                                  "descricao_produto": 1, 
                                                  "_id": 0
                                                 }).sort("descricao_produto", ASCENDING)
        df_produto = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_produto)        
        input("Pressione Enter para Sair do Relatório de Produtos")

    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["clientes"].find({}, 
                                                 {"cpf": 1, 
                                                  "RG": 1, 
                                                  "CNH": 1, 
                                                  "nome": 1, 
                                                  "endereco": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_cliente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_cliente)
        input("Pressione Enter para Sair do Relatório de Clientes")

    def get_relatorio_categoria(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["categoria"].find({}, 
                                                     {"codigo_categoria": 1, 
                                                      "descricao": 1, 
                                                      "valor_diaria": 1, 
                                                      "_id": 0
                                                     }).sort("codigo_categoria", ASCENDING)
        df_categoria = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_categoria)        
        input("Pressione Enter para Sair do Relatório de Categorias")

    def get_relatorio_alocacao(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db['alocacao'].aggregate([{
                              '$lookup': {
                                             'from': 'clientes',
                                             'localField': 'cpf',
                                             'foreignField': 'cpf',
                                             'as': 'cli'
                                         }
                             },
                             {
                              '$unwind':  { 'path': '$cli'}
                             },
                             {
                              '$lookup':{
                                             'from': 'carro',
                                             'localField': 'chassi',
                                             'foreignField': 'chassi',
                                             'as': 'car'
                                         }
                             },
                             {
                              '$unwind':  { 'path': '$car'}
                             }, 

                             
                             {
                              '$project': {'codigo_alocacao': 1,
                                           'cpf': 1,
                                           'nome':'$cli.nome',
                                           'chassi': 1,
                                           'data_saida': 1 ,
                                           'data_entrega': 1 ,
                                           '_id': 0
                                          }
                            }])
        # Converte o cursos em lista e em DataFrame
        df_alocacao = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_alocacao)
        input("Pressione Enter para Sair do Relatório de Alocações")
    

    def get_relatorio_carro(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db['carro'].aggregate([{
                                                            '$lookup':{'from':'categoria',
                                                                       'localField':'codigo_categoria',
                                                                       'foreignField':'codigo_categoria',
                                                                       'as':'cat'
                                                                      }
                                                           },
                                                           {
                                                            '$unwind':{'path': '$cat'}
                                                           },
                                                           {'$project':{'chassi':1, 
                                                                    'codigo_categoria':1,
                                                                    'valor_diaria':'$cat.valor_diaria',
                                                                    'cor':1,
                                                                    'modelo':1,
                                                                    'marca':1,
                                                                    'placa':1,
                                                                    'ano':1,
                                                                    '_id':0
                                                                    }}
                                                          ])
        # Converte o cursos em lista e em DataFrame
        df_carro = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_carro)
        input("Pressione Enter para Sair do Relatório de Carros")