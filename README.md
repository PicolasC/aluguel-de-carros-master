# Sistema de alocação de carros CRUD_MONGODB
Esse sistema de alocação de carros é composto por um conjunto de coleções(collections) que representam pedidos de vendas, contendo coleções como: clientes, categoria, alocações e carro.
O sistema exige que as coleções existam, então basta executar o script Python a seguir para criação das coleções e preenchimento de dados de exemplos:
  
      ~$ python createCollectionsAndData.py
      
Atenção: tendo em vista que esse projeto usa de base o projeto exemple crud oracle localizado em https://github.com/howardroatti/example_crud_oracle, é importante que as tabelas do Oracle existam e estejam preenchidas, pois o script createCollectionsAndData.py irá realizar uma consulta em cada uma das tabelas e preencher as collections com os novos documents.

Para executar o sistema basta executar o script Python a seguir:

      ~$ python principal.py


  
# Organização
✦ diagrams- Nesse diretório está o diagrama relacional do sistema. 
  
✧ Esse sistema possui quatro entidades: CLIENTES, CATEGORIA, ALOCAÇÕES E CARRO.

✦ src-Nesse diretório estão os scripts do sistema

✧conexion: Nesse repositório encontra-se o módulo de conexão com o banco de dados Oracle e o módulo de conexão com o banco de dados Mongo. Esses módulos possuem algumas funcionalidades úteis para execução de instruções. O módulo do Oracle permite obter como resultado das queries JSON, Matriz e Pandas DataFrame. Já o módulo do Mongo apenas realiza a conexão, os métodos CRUD e de recuperação de dados são implementados diretamente nos objetos controladores (Controllers) e no objeto de Relatório (reports).

▢Exemplo de código de inserção em Mongo:

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
            novo_cliente = Cliente(df_cliente.cpf.values[0], df_cliente.RG.values[0], df_cliente.CNH.values[0], df_cliente.nome.values[0],                              df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            self.mongo.close()
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None
            
▢Exemplo de atualização em Mongo:

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

✧controller: Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.

✧model: Nesse diretório encontram-ser as classes das entidades descritas no diagrama relacional

✧reports Nesse diretório encontra-se a classe responsável por gerar todos os relatórios do sistema

✧utils: Nesse diretório encontram-se scripts de configuração e automatização da tela de informações iniciais

✧createCollectionsAndData.py: Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script principal.py para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em alguma outra IDE de acesso ao Banco de Dados.

✧principal.py: Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

# Bibliotecas Utilizada
✦requirements.txt: *pip install -r requirements.txt*
