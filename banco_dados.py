import mysql.connector

class Banco_dados:
    def __init__(self, endereco, usuario, senha):
        self.connection = self.criar_conexao_inicial(endereco, usuario, senha)

    def criar_conexao_inicial(self, endereco, usuario, senha):
        return mysql.connector.connect(
            host=endereco,
            user=usuario,
            password=senha
        )
    def encerrarBancoDados(self):
        self.connection.close()

    def criar_banco_dados(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()

    def criar_tabela(self, nome_banco_dados, sql):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {nome_banco_dados}")
        cursor.execute(sql)
        cursor.close()
        #print(f"Tabela criada ou já existente.") - como já sei que foi criada, comentei o print para não repetir sempre que iniciar
    
    def excluir_banco_dados(self, connection, nome_banco):
        cursor = self.connection.cursor()
        cursor.execute(f"DROP DATABASE {nome_banco}")
        connection.commit()
        cursor.close()

