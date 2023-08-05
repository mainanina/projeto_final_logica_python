# Trabalho de conclusão do módulo Lógica de Programação II - Santander Coders ADA
# Autor: Maína Alexadre

import json


def lerSalvarArquivo(*dados, ler=True, nomeArquivo='projetoModuloII.json'):
    '''
        Funcão que lê ou salva um arquivo do tipo json
        Para a função de leitura, retorna-se um dicionário Python
        Para função de salvar, não há retorno
    '''
    if ler:
        try: 
            with open(nomeArquivo, encoding='utf8') as file:
                arquivo = json.load(file)
            return arquivo
        except:
            raise Exception('Erro ao ler o arquivo.')

    else:
        try:
            with open(nomeArquivo, 'w', encoding='utf8') as file:
                json.dump(dados[0], file, indent=4, ensure_ascii=False)
        except:
            raise Exception('Erro ao salvar o arquivo.')
        

dados_cadastro = lerSalvarArquivo(ler=True)


def menu(dados_cadastro):
    '''
        Função principal que inicializa o menu e faz a chamada das funções
        do programa de acordo com a opção escolhida
    '''
    menu_str = """
    Digite a opção desejada:
    1 - Inserir usuário
    2 - Excluir usuário
    3 - Atualizar usuário
    4 - Informações de alguns usuários
    5 - Informações de todos os usuários
    6 - Sair\n
    """
    opcao = input(menu_str)
    if opcao == "1":
        addUsuario(dados_cadastro)
    elif opcao == "2":
        usuarios_exclusao = selecionarUsuarios(dados_cadastro,\
            "Digite o id do usuário que deseja excluir: ", "Digite 's' se deseja excluir mais um usuário: ")
        excluirUsuario(dados_cadastro, usuarios_exclusao)
    elif opcao == "3":
        usuarios_edicao = selecionarUsuarios(dados_cadastro,\
            "Digite o id do usuário que deseja editar: ", "Digite 's' se deseja editar mais um usuário: ")
        editUsuario(dados_cadastro, usuarios_edicao)
    elif opcao == "4":
        usuarios_exibicao = selecionarUsuarios(dados_cadastro,\
            "Digite o id do usuário que deseja exibir: ", "Digite 's' se deseja exibir mais um usuário: ")
        exibirAlgunsUsuarios(dados_cadastro, usuarios_exibicao)
    elif opcao == "5":
        exibirTodosUsuarios(dados_cadastro)
    elif opcao == "6":
        encerrarPrograma(dados_cadastro)
    else:
        print(f"Opção digitada ({opcao}) inválida")
        menu(dados_cadastro)


def addUsuario(dados):
    '''
        Adiciona usuários ao arquivo .json original de acordo com dados fornecidos
        através da interface com o usuário
    '''
    continuar = 's'
    while continuar.lower()=='s':
        maior_id = max(dados.keys())
        nome = input("Digite o nome do usuário: ")
        tem_tel = input("Digite 's' se deseja incluir um número de telefone: ")
        telefone = "Nao informado"
        endereco = "Nao informado"
        if tem_tel.lower()=='s':
            telefone = input("Digite um telefone: ")
        tem_end = input("Digite 's' se deseja incluir um endereço: ")
        if tem_end.lower()=='s':
            endereco = input("Digite um endereço: ")
        existe_usuario, id = verificarUsuario(nome, endereco, telefone, dados)
        if existe_usuario:
            dados[id]["Status"]=True
            print(f"Usuário {dados[id]['Nome']} reativado.")
        else:    
            dados[str(int(maior_id)+1)] = {
                "Status": True,
                "Nome": nome,
                "Telefone": telefone,
                "Endereço": endereco
            }
            print(f"Usuário {nome} adicionado.")
        continuar = input("Digite 's' se deseja inserir novos usuários: ")
    menu(dados_cadastro)


def verificarUsuario(nome, endereco, telefone, dicionario):
    '''
        Verifica se o usuário já existe com as mesmas informações cadastradas;
        Caso ele exista, retorna True e o id do usuário
    '''
    for id, valor in dicionario.items():
        if valor["Nome"] == nome and valor["Telefone"] == telefone and valor["Endereço"]==endereco and valor["Status"]==False:
            return True, id
    return False, ""


def selecionarUsuarios(dados, pergunta1, pergunta2):
    '''
        Função que faz interface com usuário para selecionar quais usuários excluir
    '''
    lista = []
    continuar = "s"
    while continuar.lower() == "s":
        id = input(pergunta1)
        if id in dados.keys() and dados[id]['Status']:
            lista.append(id)
        else:
            print("Usuário não encontrado!")
        continuar = input(pergunta2)
    return lista


def excluirUsuario(dados, usuarios):
    '''
        Recebe uma lista dos ids dos cadastros que o usuário deseja deletar e 
        os apaga do arquivo original
    '''
    for id in usuarios:
        dados[id]["Status"] = False
        print(f"Usuário {id} foi inativado.")
    menu(dados)


def editUsuario(dados, usuarios):
    '''
        Recebe uma lista dos ids dos cadastros que o usuário deseja editar, pergunta
        ao usuário qual o item do cadastro a ser modificado e o altera
    '''
    for id in usuarios:
        opcao = "0"
        item = ""
        nova_info = ""
        sub_menu = f"""
        \nQual informação deseja alterar para o usuario {id}?
        1 - Nome
        2 - Tefone
        3 - Endereço
        """
        while opcao == "0":
            opcao = input(sub_menu)
            if opcao == "1":
                item = "Nome"
                nova_info = input("Insira o novo nome: ")
            elif opcao == "2":
                item = "Telefone"
                nova_info = input("Insira o novo telefone: ")
            elif opcao == "3":
                item = "Endereço"
                nova_info = input("Insira o novo endereço: ")
            else: 
                print("Opção inválida")
                opcao = "0"

        dados[id][item] = nova_info
        print(f"Usuario {id} atualizado.")
    menu(dados_cadastro)


def exibirAlgunsUsuarios(dados, usuarios):
    '''
        Exibe os dados dos usuários selecionados pelo usuário através da lista 
        de ids que recebe
    '''
    for id in usuarios:
        print("-----------------------------------------------")
        print(f"Nome: {dados[id]['Nome']}")
        print(f"Telefone: {dados[id]['Telefone']}")
        print(f"Endereço: {dados[id]['Endereço']}")
        print("-----------------------------------------------")
    menu(dados_cadastro)


def exibirTodosUsuarios(dados):
    '''
        Exibe os dados de todos usuários existentes no cadastro
    '''
    for id in dados.keys():
        if dados[id]['Status']:
            print("-----------------------------------------------")
            print(f"ID: {id}")
            print(f"Nome: {dados[id]['Nome']}")
            print(f"Telefone: {dados[id]['Telefone']}")
            print(f"Endereço: {dados[id]['Endereço']}")
            print("-----------------------------------------------")
    menu(dados_cadastro)


def encerrarPrograma(dados, nomeArquivo='projetoModuloII.json'):
    '''
        Função que encerra o programa salvando os dados no arquivo .json
    '''
    lerSalvarArquivo(dados, ler=False)
    print("Obrigado por utilizar nosso programa!\n")


if __name__ == '__main__':
    print("\nBoas-vindas ao nosso sistema!")
    menu(dados_cadastro)
