from animal import Animal
from adotante import Adotante
from datetime import datetime, date
import re

class Ong:

    def __init__(self, conexao):
        self.connection = conexao

    def validar_entrada(self, prompt, tipo=str):
        while True:
            entrada = input(prompt).strip()
            if tipo == str:
                if entrada:
                    return entrada.title()
                else:
                    print("Campo vazio. Por favor, preencha novamente.")
            elif tipo == int:
                try:
                    return int(entrada)
                except ValueError:
                    print("Valor inválido, por favor digite o número(ou números) novamente.")
    
    def validar_cpf(self, prompt):
        
        while True:
            cpf = input(prompt)
            cpf_str = str(cpf)
            
            if len(cpf_str) != 11:
                print("CPF Inválido!")
                continue
            try:
                cursor = self.connection.cursor()
                sql = "SELECT COUNT(*) FROM adotantes WHERE cpf = %s"
                cursor.execute(sql, (cpf_str,))
                resultado = cursor.fetchone()
                if resultado[0] > 0:
                    print("CPF já está cadastrado.")
                    continue
                else:
                    return cpf_str
            finally:
                cursor.close()

    def validar_contato(self, prompt):
        while True:
            entrada = input(prompt).strip()
            if re.match(r'^\(\d{2}\)9\d{4}-\d{4}$', entrada):
                return entrada
            else:
                print("Formato inválido. Use o formato (DD)9xxxx-xxxx.")
                
    def cadastrar_adotante(self):
        cursor = self.connection.cursor()

        nome = self.validar_entrada("Digite o nome: ")
        cpf = self.validar_cpf("CPF (Somente números): ")
        endereco = self.validar_entrada("Endereço (Rua - N° - Bairro - Cidade/Estado): ")
        contato = self.validar_contato("Número para contato (Formato: (DD)9xxxx-xxxx): ")
        animais_adotados = ""

        adotante = Adotante(nome, cpf, endereco, contato, animais_adotados)
        dados_adotante = [adotante.nome, adotante.cpf, adotante.endereco, adotante.contato, adotante.animais_adotados]
        sql = "INSERT INTO adotantes (nome, cpf, endereco, contato, animais_adotados) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, dados_adotante)
            self.connection.commit()
            print("Usuário cadastrado com sucesso!\n")
        except Exception as e:
            print(f"Erro ao cadastrar adotante: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def formato_lista_adotantes(self, adotante):
        return (
            f"N° de Identificação: {adotante[0]}\n"
            f"- Nome: {adotante[1]}\n"
            f"- CPF: {adotante[2]}\n"
            f"- Endereço: {adotante[3]}\n"
            f"- Contato: {adotante[4]}\n"
            f"- Animais adotados: {adotante[5]}\n\n"
        )
    
    def listar_adotantes(self):
        sql = "SELECT id, nome, cpf, endereco, contato, animais_adotados FROM adotantes"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        adotantes = cursor.fetchall()
        cursor.close()

        if not adotantes:
            return "Nenhum usuário cadastrado."

        lista_adotantes = ""
        for adotante in adotantes:
            lista_adotantes += self.formato_lista_adotantes(adotante)
        return lista_adotantes
           
    def validar_entrada_opcoes(self, prompt, opcao_valida):
        while True:
            texto = input(prompt).capitalize()
            if texto in opcao_valida:
                return texto
            else:
                print(f"Entrada inválida. Por favor, digite uma das opções!")
    
    def calcular_idade(self, data_nascimento_str):

        dia, mes, ano = map(int, data_nascimento_str.split("/"))
        data_nascimento = date(ano, mes, dia)
        data_atual = date.today()
        dias = data_atual - data_nascimento
        idade = dias.days // 365
        
        return idade
    
    def calcular_idade_meses(self, data_nascimento_str):
        dia, mes, ano = map(int, data_nascimento_str.split("/"))
        data_nascimento = date(ano, mes, dia)
        data_atual = date.today()
        dias = (data_atual - data_nascimento).days
        meses = (dias % 365) // 30

        return meses

    def cadastrar_animal(self):
        cursor = self.connection.cursor()

        nome = self.validar_entrada("Digite o nome do animal: ").capitalize()
        while True:
            data_nascimento_str = input("Data de nascimento (Formato: DD/MM/AAAA): ")
            try:
                data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y").date()
                break 
            except ValueError:
                print("Formato de data inválido! Use DD/MM/AAAA.")

        idade = self.calcular_idade(data_nascimento_str)
        meses = self.calcular_idade_meses(data_nascimento_str)
        especie = self.validar_entrada_opcoes("Digite a espécie (Gato ou Cachorro): ", ["Gato", "Cachorro"])
        genero = self.validar_entrada_opcoes("Gênero (Macho ou Fêmea): ", ["Macho", "Fêmea", "Femea"])
        porte = self.validar_entrada_opcoes("Porte (Pequeno, Médio ou Grande): ", ["Pequeno", "Médio", "Grande"])
        pelagem = self.validar_entrada("Descreva a pelagem do animal: ").capitalize()
        observacoes = input("Observações do animal (Espaço livre): ").capitalize()

        animal = Animal(nome, data_nascimento, idade, meses, especie, genero, porte, pelagem, observacoes)
        dados_animal = [animal.nome, animal.data_nascimento, animal.idade, animal.meses, animal.especie, animal.genero, animal.porte, animal.pelagem, animal.observacoes]
        sql = "INSERT INTO animais (nome, data_nascimento, idade, meses, especie, genero, porte, pelagem, observacoes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, dados_animal)
        self.connection.commit()
        
        print("\nAnimal cadastrado com sucesso!\n")
        cursor.close()

    def checar_existencia_animais(self):
        sql = "SELECT * FROM animais"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        animais = cursor.fetchall()
        cursor.close()
        
        if not animais:
            print("Nenhum animal cadastrado para adoção!")
            return False
        return True

    def formato_lista_animais(self, animal):
        return (
            f'N° de Identificação: {animal[0]}\n'
            f'- Nome: {animal[1]}\n'
            f'- Data de Nascimento: {animal[2]}\n'
            f'- Idade: {animal[3]} ano(s) e {animal[4]} mes(es)\n'
            f'- Espécie: {animal[5]}\n'
            f'- Gênero: {animal[6]}\n'
            f'- Porte: {animal[7]}\n'
            f'- Pelagem: {animal[8]}\n'
            f'- Observações: {animal[9]}\n\n'
        )       
    def listar_animais(self):
        sql = "SELECT * FROM animais"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        animais = cursor.fetchall()
        cursor.close()

        if not animais:
            return "Nenhum animal cadastrado.\n"
        
        lista_animais = ""
        for animal in animais:
            lista_animais += self.formato_lista_animais(animal)
        return lista_animais
    
    def filtrar_animal(self):
        print("Caso não deseje aplicar um dos filtros, deixe a opção em branco.")

        especie = self.validar_entrada_opcoes("Digite a espécie (Gato ou Cachorro): ", ["Gato", "Cachorro", ""])
        porte = self.validar_entrada_opcoes("Porte (Pequeno, Médio ou Grande): ", ["Pequeno", "Médio", "Grande", "", "Medio"])
        genero = self.validar_entrada_opcoes("Gênero (Macho ou Fêmea): ", ["Macho", "Fêmea", "Femea", ""])
        idade_str = input("Idade máxima do animal: ")
        
        sql = "SELECT * FROM animais WHERE 1=1"
        parametros = []

        if especie:
            sql += " AND especie = %s"
            parametros.append(especie)

        if porte:
            sql += " AND porte = %s"
            parametros.append(porte)

        if genero:
            sql += " AND genero = %s"
            parametros.append(genero)

        if idade_str:
            try:
                idade = int(idade_str)
                sql += " AND idade <= %s"
                parametros.append(idade)
            except ValueError:
                print("Idade inválida. Não foi aplicado filtro de idade.")

        cursor = self.connection.cursor()
        cursor.execute(sql, parametros)
        animais = cursor.fetchall()
        cursor.close()

        lista_animais = "-- Animais encontrados: --\n"
        id_animais_filtrados = []
        for animal in animais:
            id_animais_filtrados.append(animal[0])
            lista_animais += self.formato_lista_animais(animal)
        
        return lista_animais, id_animais_filtrados
    
    def adotar_animal(self):
            
            if not self.checar_existencia_animais():
                return          

            id_adotante = self.validar_entrada("Digite o N° de Identificação do Adotante: ", tipo=int)
            sql = "SELECT id, nome FROM adotantes WHERE id = %s" 
            cursor = self.connection.cursor()
            cursor.execute(sql, (id_adotante,))
            adotantes = cursor.fetchall()
        
            if len(adotantes) == 0:
                print("Usuário não encontrado!\n")
                cursor.close()
                return
            else:
                lista_adotantes = "-- Usuário encontrado --\n"
                for adotante in adotantes:
                    lista_adotantes += (
                        f'N° de Identificação: {adotante[0]}\n'
                        f'- Nome: {adotante[1]}\n'
                    )
                print(lista_adotantes)

                lista_animais, id_animais_filtrados = self.filtrar_animal()
                print(lista_animais)

                if not id_animais_filtrados:
                    print("Nenhum animal disponível para adoção com um (ou mais) dos filtros aplicados.")
                    return

                print("-- Qual animal deseja adotar? --")
                
                id_animal = self.validar_entrada("Digite o N° de Identificação do animal: ", tipo=int)
                if id_animal not in id_animais_filtrados:
                    print("ID - Animal não encontrado.")
                    return

                sql_dados_animal = "SELECT * FROM animais WHERE id = %s"
                cursor.execute(sql_dados_animal, (id_animal,))
                animal = cursor.fetchone()

                confirmar_animal = self.formato_lista_animais(animal)
                print("\nEsse é o animal que deseja adotar?\n" + confirmar_animal)
                confirmar = self.validar_entrada_opcoes("Sim ou não: ", ["Sim", "Não", "Nao"])
                if confirmar != "Sim":
                    print("Adoção cancelada.")
                    cursor.close()
                    return
                
                sql_delete_animal = "DELETE FROM animais WHERE id = %s"
                cursor.execute(sql_delete_animal, (id_animal,))
                self.connection.commit()

                sql_animais_adotados = "SELECT animais_adotados FROM adotantes WHERE id = %s"
                cursor.execute(sql_animais_adotados, (id_adotante,))
                animais_adotados = cursor.fetchone()[0]

                if animais_adotados:
                    animais_adotados += f"\n{animal[1]} (ID: {animal[0]}) - {animal[3]} ano(s) e {animal[4]} mes(es) - \
{animal[5]} - {animal[6]} - {animal[7]} - Pelagem: {animal[8]} - Obs: {animal[9]}"
                else:
                    animais_adotados = f"{animal[1]} (ID: {animal[0]}) - {animal[3]} ano(s) e {animal[4]} mes(es) - {animal[5]} - \
{animal[6]} - {animal[7]} - Pelagem: {animal[8]} - Obs: {animal[9]}"

                sql_update = "UPDATE adotantes SET animais_adotados = %s WHERE id = %s"
                cursor.execute(sql_update, (animais_adotados, id_adotante))
                self.connection.commit()

                nome_adotante = ""
                for adotante in adotantes:
                    if adotante[0] == id_adotante:
                        nome_adotante = adotante[1]
                        break

                print("Adoção concluída com sucesso!\n")
                self.historico_adocao(id_adotante, nome_adotante, id_animal, animal[1])
                cursor.close()
             
    def historico_adocao(self, id_adotante, nome_adotante, id_animal, nome_animal):
        try:
            with open('historico_adocoes.txt', 'a', encoding="utf-8") as f:
                data_hora = datetime.now().strftime("%d/%m/%Y")
                historico = f'{data_hora} - Adotante: {nome_adotante} com ID: {id_adotante} - Animal adotado: {nome_animal} com ID: {id_animal}\n'
                f.write(historico)
                print("E histórico registrado!\n")
        except Exception as e:
            print(f"Erro ao registrar histórico de adoção: {e}")

    def alterar_observacoes(self):

        if not self.checar_existencia_animais():
            return

        id_animal = self.validar_entrada("Digite o N° de Identificação do animal: ", tipo=int)
        
        sql = "SELECT * FROM animais WHERE id = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql, (id_animal,))
        animal = cursor.fetchone()

        if not animal:
            print("Nenhum animal encontrado!")
            cursor.close()
            return 
        
        lista_animais = "-- Animais encontrados --\n"
        lista_animais += self.formato_lista_animais(animal)
        print(lista_animais)

        if animal[9] is None:
            observacao_existente = ""
        else:
            observacao_existente = animal[9]
        
        nova_observacao = self.validar_entrada("Digite a nova observação a ser adicionada: ")
        observacoes_atualizadas = (observacao_existente + " - " + nova_observacao).strip()
        
        sql_update = "UPDATE animais SET observacoes = %s WHERE id = %s"
        cursor.execute(sql_update, (observacoes_atualizadas, id_animal))
        self.connection.commit()

        print("Observações atualizadas com sucesso!\n")
        cursor.close()


        
        
