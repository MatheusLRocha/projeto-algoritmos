import base64 # Mexe com codificação e decodificação de dados
import os # Mexe com arquivos e diretórios
from cryptography.fernet import Fernet # Criptografia simétrica, cria uma chave para descriptografar e criptografar dados
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id # Derivação de chaves(KDF)

class GerenciadorDeSenhas:
    # Criação do constructor
    def __init__(self):
        self.arquivo_senhas = None
        self.isLogged = False
        self.senhas = {}
        self.fernet = None
        
    # Gera chave de criptografia com base na senha mestre e salt.    
    def gerar_chave(self, senha_mestre, salt):
        # Código feito a partir da documentação do fernet e do argon2id, ambos da biblioteca cryptography
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=1,
            lanes=4,
            memory_cost=2**21
        )

        # Retorna a chave gerada a partir da senha mestre e do salt, codificada em base64 para ser usada pelo fernet
        return base64.urlsafe_b64encode(kdf.derive(senha_mestre.encode()))

    # O usuário precisa indicar onde vai salvar a senha mais importante dele
    def criar_conta(self, passphrase):
        # salt é gerado aleatoriamente
        salt = os.urandom(16)

        # Gera a chave e criptografia e coloca ela no fernet
        key = self.gerar_chave(passphrase, salt)
        self.fernet = Fernet(key)

        # Cria um arquivo para salvar o salt e outro para salvar a senha criptografada de autenticação
        with open('salt.txt', 'wb') as f:
            f.write(salt)

        with open('autenticacao.txt', 'w') as f:
            texto_cofre = self.fernet.encrypt(b'Cofre criado')
            f.write(texto_cofre.decode() + '\n')

        # Após criar a conta, o usuário já está logado
        self.isLogged = True

    # Verifica se o usuário tem uma conta
    def login_conta(self, senha_mestra):
        # Pega o salt armazenado
        with open('salt.txt', 'rb') as f:
            salt = f.read()

        # Gera a chave de criptografia a partir da senha mestre e do salt, e coloca ela no fernet
        key = self.gerar_chave(senha_mestra, salt)
        self.fernet = Fernet(key)

        # Pega a autenticação criptografada armazenada
        with open('autenticacao.txt', 'r') as f:
            dados_criptografados = f.readline()

        try:
            # Descriptografa a autenticação para verificar se a senha mestre está correta
            dados_descriptografados = self.fernet.decrypt(dados_criptografados.encode())

            # Se estiver, o usuário é logado e as senhas salvas são carregadas para a memória
            self.isLogged = True

            print('Login feito com sucesso!')

            try:
                # Abre o cofre de senhas e armazena todas elas em um dicionário para facilitar o acesso
                with open('senhas.txt', 'r') as f:
                    for line in f:
                        key, value = line.split(':')

                        self.senhas[self.fernet.decrypt(key).decode()] = self.fernet.decrypt(value).decode()
            except:
                print('Ainda não há senhas no cofre')
        except:
            print('Login negado')

    # Sai da conta e fecha o aplicativo
    def sair_conta(self):
        self.isLogged = False
            
    # Mostra todas as senhas criadas se estiver logado
    def ver_senhas(self):
        try:
            if self.isLogged:
                with open('senhas.txt', 'r') as f:
                    for line in f:
                        site, senha = line.split(':')
                        print(self.fernet.decrypt(site.encode()).decode() + ' - ' + self.fernet.decrypt(senha.encode()).decode())
            else:
                print('Você não possui acesso, verifique seu login')
        except:
            print('Ainda não há um arquivo de senhas criado')
        

    # Permite criar uma senha nova se estiver logado
    def criar_nova_senha(self, site, password):
        if self.isLogged:
            # Criptografa o nome do site e a senha
            encrypted_site = self.fernet.encrypt(site.encode())
            encrypted_password = self.fernet.encrypt(password.encode())

            # Salva a senha criptografada no arquivo de senhas, junto com o nome do site criptografado
            with open('senhas.txt', 'a+') as f:
                f.write(f'{encrypted_site.decode()}:{encrypted_password.decode()}\n')

            # Armazena a senha no dicionário de senhas para facilitar o acesso
            self.senhas[site] = password
        else:
            print('Você não possui acesso, verifique seu login')
        

    # Buscar uma das senhas se estiver logado
    def buscar_senha(self, site):
        if self.isLogged:
            try:
                print(self.senhas[site])
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

            pm.criar_conta(senha)
        case 2:
            senha = input('Digite sua senha: ')
            pm.login_conta(senha)
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