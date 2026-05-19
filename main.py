import base64 # Mexe com codificação e decodificação de dados
import os # Mexe com arquivos e diretórios
from cryptography.fernet import Fernet # Criptografia simétrica, cria uma chave para descriptografar e criptografar dados
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id # Derivação de chaves(KDF)
from database import Password, db # Importa a classe Password e o banco de dados do arquivo database.py

class ConexaoBancoDeDados:
    def __init__(self):
        db.connect() # Conecta ao banco de dados
        db.create_tables([Password]) # Cria a tabela de senhas no banco de dados, caso ela ainda não exista

    # CRUD(Create, Read, Update, Delete) para manipular os dados do banco de dados utilizando a classe Password

    def adicionar_senha(self, title, password):
        # Cria um novo registro de senha no banco de dados utilizando a classe Password
        Password.create(title=title, password=password) 

    def listar_senhas(self):
        # Retorna todas as senhas armazenadas no banco de dados
        return Password.select()
    
    def buscar_senha(self, title):
        return Password.get_or_none(Password.title == title)
    
    def atualizar_senha(self, title, new_password):
        ...

    def deletar_senha(self, title):
        ...

        

class GerenciadorDeSenhas:
    # Criação do constructor
    def __init__(self, banco):
        self.banco = banco
        self.isLogged = False
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

            print('Login feito com sucesso!')

            self.isLogged = True
            return self.isLogged
        except:
            print('Login negado')

            self.isLogged = False
            return self.isLogged

    # Sai da conta e fecha o aplicativo
    def sair_conta(self):
        self.isLogged = False
            
    # Mostra todas as senhas criadas se estiver logado
    def ver_senhas(self):
        try:
            if self.isLogged:
                senhas = self.banco.listar_senhas()

                for senha in senhas:
                    print(f'{self.fernet.decrypt(senha.title.encode()).decode()}: {self.fernet.decrypt(senha.password.encode()).decode()}')
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

            # Salva a senha criptografada no banco de dados utilizando a função adicionar_senha da Classe ConexaoBancoDeDados
            self.banco.adicionar_senha(encrypted_site.decode(), encrypted_password.decode())
        else:
            print('Você não possui acesso, verifique seu login')
        

    # Buscar uma das senhas se estiver logado
    def buscar_senha(self, site):
        if self.isLogged:
            try:
                senha = None

                # Descriptografa cada senha do banco de dados e compara com o site, buscando valor válido, se encontrar, retorna a senha descriptografada
                for item in self.banco.listar_senhas():
                    if self.fernet.decrypt(item.title.encode()).decode() == site:
                        senha = self.fernet.decrypt(self.banco.buscar_senha(item.title).password.encode()).decode()

                # Se existir a senha, exibe ela
                if senha is not None:
                    print(f'Senha: {senha}')
                else:
                    print('Senha não encontrada')
                    return None
            except:
                print('Ainda não há um arquivo de senhas criado')
            
        else:
            print('Você não possui acesso, verifique seu login')
        
        

# Instancia o gerenciador de senhas para acessar as funções de login e gerenciamento de senhas
pm = GerenciadorDeSenhas(ConexaoBancoDeDados())

if __name__ == '__main__':
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