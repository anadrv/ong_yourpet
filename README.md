# Sistema de gerenciamento de animais para uma ONG

Trabalho desenvolvido para disciplina de "Programar em linguagem estruturada" 

1. Cadastrar um novo animal. Um animal deve conter as informações: identificador (número ou código) [automático], nome, data de nascimento aproximada, espécie (cachorro ou gato), porte, pelagem, sexo, observações (texto livre)

2. Listar animais disponíveis para adoção. Ao listar os animais, o sistema deve imprimir todas as informações de um animal.

3. Adotar animal. A função de adotar um animal requer que o usuário informe o id do adotante, e em seguida a espécie, o porte, o sexo e a idade máxima  do animal (o usuário também pode não digitar nada se não quiser algum dos filtros). Então, o sistema imprime uma listagem filtrada dos animais que respeitam os parâmetros informados. O usuário pode, então, escolher um animal através de seu identificador. Por fim, o animal é removido da lista.

4. Cadastrar adotante (id [automático], nome completo, cpf, endereço, contato, lista de animais adotados)

5. Listar adotantes. Lista todos os adotantes e suas informações.

6. Alterar observações de um animal.

7. Histórico de adoções. Histórico simples com todas as adoções que já aconteceram. (Adotante X (id) adotou Animal Y (id)).


Por fim, deve haver persistência de dados utilizando banco de dados. O banco de dados deve ser atualizado após cada operação de cadastro, atualização ou remoção.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
