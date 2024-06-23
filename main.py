from banco_dados import Banco_dados
from sistema_ong import Ong

class Main:
    def __init__(self):
        self.banco = Banco_dados("local", "user", "senha")
        self.banco.criar_banco_dados("CREATE DATABASE IF NOT EXISTS ONG_YourPet")
        self.banco.criar_tabela("ONG_YourPet", """
            CREATE TABLE IF NOT EXISTS animais (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50),
                data_nascimento DATE,
                idade INT,
                meses INT,
                especie VARCHAR(10),
                genero VARCHAR(50),
                porte VARCHAR(10),
                pelagem VARCHAR(30),
                observacoes VARCHAR(200)
            )
        """)
        self.banco.criar_tabela("ONG_YourPet", """
            CREATE TABLE IF NOT EXISTS adotantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50),
                cpf VARCHAR(20),
                endereco VARCHAR(200),
                contato VARCHAR(15),
                animais_adotados VARCHAR(500)
            )
        """)
        self.conexao = self.banco.criar_conexao_inicial("local", "user", "senha")
        self.sistema_ong = Ong(self.banco.connection)

    def executar(self):
        while True:
            try:
                print("-- ONG YourPet || Menu de opções --\n\n"
                        "1 - Cadastrar usuário \n"
                        "2 - Cadastrar animal para adoção \n"
                        "3 - Animais disponíveis para adoção \n"
                        "4 - Adotar animal \n"
                        "5 - Usuários cadastrados \n"
                        "6 - Alterar observações do animal\n"
                        "7 - Histórico de adoções \n"
                        "8 - Sair do sistema \n")
                
                opcao = int(input("Digite a opção desejada: "))

                if opcao == 1:
                    print("-- Cadastro usuário --\n")
                    self.sistema_ong.cadastrar_adotante()

                elif opcao == 2:
                    print("-- Cadastro do animal --\n")
                    self.sistema_ong.cadastrar_animal()
                
                elif opcao == 3:
                    print("-- Lista de animais disponívies para adoção --\n")
                    print(self.sistema_ong.listar_animais())

                elif opcao == 4:
                    print("-- Adoção --\n")
                    self.sistema_ong.adotar_animal()

                elif opcao == 5:
                    print("-- Lista de usuários cadastrados --\n")
                    print(self.sistema_ong.listar_adotantes())
                
                elif opcao == 6:
                    self.sistema_ong.alterar_observacoes()
                    
                elif opcao == 7:
                    print("-- Histórico de adoções --\n")
                    try:
                        with open('historico_adocoes.txt', 'r', encoding="utf-8") as f:
                            historico = f.read()
                            if historico.strip() == "":
                                print("Nenhum histórico encontrado.\n")
                            else:
                                print(historico)
                    except FileNotFoundError:
                        print("Nenhum histórico de adoções encontrado.")
                    except Exception as e:
                        print(f"Erro ao ler histórico de adoções: {e}")
                    
                elif opcao == 8:
                    print("-- ONG YourPet -- Fim do sistema!")
                    break
                else:
                    print("Opção inválida!")

            except ValueError:
                print ("Opção inválida - Por favor digite uma das opções do menu!")
                continue
            
main = Main()
main.executar()


