from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):


        # Nome(s) do(s) criador(es)
        self.created_by = "GUILHERME NOGUEIRA DESSAUNE DE OLIVEIRA"
        self.created_by2 = "KAYO VINICIUS SILVA BRAGA"
        self.created_by3 = "DAVI BRAGA BRAUNN"
        self.created_by4 = "EDUARDO SPERANDIO OLIVEIRA"
        self.created_by5 = "RAMON PESSIN DA SILVA"
        self.disciplina = "Banco de Dados"
        self.semestre = "2022/2"

    def get_documents_count(self, collection_name):
        # Retorna o total de registros computado pela query
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]
   

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE VENDAS                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - CATEGORIAS:  {str(self.get_documents_count(collection_name="categoria")).rjust(5)}
        #      2 - CLIENTES     {str(self.get_documents_count(collection_name="clientes")).rjust(5)}
        #      3 - CARROS:      {str(self.get_documents_count(collection_name="carro")).rjust(5)}
        #      4 - ALOCAÇÕES:   {str(self.get_documents_count(collection_name="alocacao")).rjust(5)}
        #
        #  CRIADO POR:    {self.created_by}
        #                 {self.created_by2}
        #                 {self.created_by3}
        #                 {self.created_by4}
        #                 {self.created_by5}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """