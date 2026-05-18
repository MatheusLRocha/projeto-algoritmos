import bcrypt
from cryptography import Fernet

class GerenciadorDeSenhas:
    # Criação do constructor
    def __init__(self):
        self.arquivo_senhas = None
        self.isLogged = False
        self.senhas = {}
        self.key = None

    # O usuário precisa indicar onde vai salvar a senha mais importante dele
    def criar_conta(self, senha_mestra, path):
        hash_senha = bcrypt.hashpw(senha_mestra.encode(), bcrypt.gensalt())

        with open(path, 'wb') as f:
            f.write(hash_senha)

    # Verifica se o usuário tem uma conta
    def login_conta(self, path, senha):
        try:
            # Acessa a chave mestra para comparar
            with open(path, 'rb') as f:
                chave_mestra = f.read()

            # Compara a senha digitada com a chave mestra
            if bcrypt.checkpw(senha.encode(), chave_mestra):
                print("Login realizado!")
                self.isLogged = True

                with open('senhas.txt', 'r') as f:
                    for line in f:
                        key, value = line.split(':')
                        self.senhas[key] = value
        except:
            print('Conta não encontrada, certifique-se de que uma foi criada')

    # Sai da conta e fecha o aplicativo
    def sair_conta(self):
        self.isLogged = False
            
    # Mostra todas as senhas criadas se estiver logado
    def ver_senhas(self):
        if self.isLogged:
            with open('senhas.txt', 'r') as f:
                for line in f:
                    site, senha = line.split(':')
                    print(f'{site}: {senha}')
        else:
            print('Você não possui acesso, verifique seu login')
        

    # Permite criar uma senha nova se estiver logado
    def criar_nova_senha(self, site, password):
        if self.isLogged:
            with open('senhas.txt', 'a+') as f:
                f.write(f'{site}:{password}\n')
        else:
            print('Você não possui acesso, verifique seu login')
        

        self.senhas[site] = password

    # Buscar uma das senhas se estiver logado
    def buscar_senha(self, site):
        if self.isLogged:
            try:
                print(f'Senha: {self.senhas[site]}')
            except:
                print('Falha ao buscar senha')
        else:
            print('Você não possui acesso, verifique seu login')
        
        

pm = GerenciadorDeSenhas()

while True:
    print('(1) Criar conta\n(2) Entrar na conta\n(3) Criar nova senha\n(4) Ver senhas\n(5) Buscar senha\n(6) Sair')

    opcao = int(input('Escolha uma opção: '))

    match(opcao):
        case 1:
            senha = input('Digite uma senha segura: ')
            caminho = input('Digite o lugar que deseja guardar a sua senha mestra: ')

            pm.criar_conta(senha, caminho)
        case 2:
            caminho = input('Caminho da chave mestra: ')
            senha = input('Digite sua senha: ')
            pm.login_conta(caminho, senha)
        case 3:
            site = input('Nome do site: ')
            senha = input('Senha que será salva: ')

            pm.criar_nova_senha(site, senha)
        case 4:
            pm.ver_senhas()
        case 5:
            site = input('Digite o site que se deseja buscar: ')
            pm.buscar_senha(site)
        case 6:
            print('Saindo...')
            pm.sair_conta()
            break
        case _:
            print('Valor inválido')