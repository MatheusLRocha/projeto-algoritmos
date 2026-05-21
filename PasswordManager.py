from PasswordBank import PasswordRepository
import base64 # Mexe com codificação e decodificação de dados
import os # Mexe com arquivos e diretórios
from cryptography.fernet import Fernet # Criptografia simétrica, cria uma chave para descriptografar e criptografar dados
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id # Derivação de chaves(KDF)
import random # biblioteca para aleatorizar os valores para senha aleatória

class PasswordService:
    # Criação do constructor
    def __init__(self, banco):
        self.banco = banco
        self.isLogged = False
        self.fernet = None
        
    # Gera chave de criptografia com base na senha mestre e salt.    
    def generate_key(self, master_password, salt):
        # Código feito a partir da documentação do fernet e do argon2id, ambos da biblioteca cryptography
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=1,
            lanes=4,
            memory_cost=2**21
        )


        # Retorna a chave gerada a partir da senha mestre e do salt, codificada em base64 para ser usada pelo fernet
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    # O usuário precisa indicar onde vai salvar a senha mais importante dele
    def criar_conta(self, passphrase):
        # salt é gerado aleatoriamente
        salt = os.urandom(16)

        # Gera a chave e criptografia e coloca ela no fernet
        key = self.generate_key(passphrase, salt)
        self.fernet = Fernet(key)

        # Deleta as senhas da conta antiga e cria uma nova tabela de senhas
        self.banco.new_register()

        # Cria um arquivo para salvar o salt e outro para salvar a senha criptografada de autenticação
        with open('salt.txt', 'wb') as f:
            f.write(salt)

        with open('autenticacao.txt', 'wb') as f:
            safe_text = self.fernet.encrypt(b'Cofre criado')
            f.write(safe_text)

        # Após criar a conta, o usuário já está logado
        self.isLogged = True

    # Verifica se o usuário tem uma conta
    def login_conta(self, master_password):
        # Pega o salt armazenado
        with open('salt.txt', 'rb') as f:
            salt = f.read()

        # Gera a chave de criptografia a partir da senha mestre e do salt, e coloca ela no fernet
        key = self.generate_key(master_password, salt)
        self.fernet = Fernet(key)

        # Pega a autenticação criptografada armazenada
        with open('autenticacao.txt', 'rb') as f:
            encrypted_data = f.readline()

        try:
            # Descriptografa a autenticação para verificar se a senha mestre está correta
            self.fernet.decrypt(encrypted_data)

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
        self.fernet = None

    # Permite criar uma senha nova se estiver logado
    def new_password(self, title, password):
        if self.isLogged:
            # Criptografa o nome do site e a senha
            encrypted_title = self.fernet.encrypt(title.encode())
            encrypted_password = self.fernet.encrypt(password.encode())

            # Salva a senha criptografada no banco de dados utilizando a função adicionar da Classe PasswordRepository
            self.banco.add(encrypted_title.decode(), encrypted_password.decode())
        else:
            print('Você não possui acesso, verifique seu login')
            
    # Mostra todas as senhas criadas se estiver logado
    def show_passwords(self):
        try:
            if self.isLogged:
                encrypted_passwords = self.banco.list()

                return encrypted_passwords
            else:
                print('Você não possui acesso, verifique seu login')
        except:
            print('Ainda não há um arquivo de senhas criado')

    def update_password(self, id, new_password):
        if self.isLogged:
            try:
                encrypted_new_password = self.fernet.encrypt(new_password.encode())
                
                self.banco.update(id, encrypted_new_password.decode()) # podemos atulizar a criptografia do titulo também(opcional)
            except:
                print('Ainda não há um arquivo de senhas criado')
        else:
            print('Você não possui acesso, verifique seu login')
    
    def delete_password(self, title):
        if self.isLogged:
            try:
                for item in self.banco.list():
                    if self.fernet.decrypt(item.title.encode()).decode() == title:
                        self.banco.delete(item.title)
            except:
                print('Ainda não há um arquivo de senhas criado')
        else:
            print('Você não possui acesso, verifique seu login')

    def random_password(self):
        lowercase_caracters = 'abcdefghijklmnopqrstuvwxyz'
        uppercase_caracters = lowercase_caracters.upper()
        special_caracters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        numbers = '0123456789'

        all_caracters = lowercase_caracters + uppercase_caracters + special_caracters + numbers

        # join() permite juntar todos os itens de um iterável e juntá-los em uma string
        password = ''.join(random.choices(all_caracters, k=20))



if __name__ == '__main__':
    # Instancia o gerenciador de senhas para acessar as funções de login e gerenciamento de senhas
    banco = PasswordRepository()
    pm = PasswordService(banco)

    while True:
        print('(1) Criar conta\n(2) Entrar na conta\n(3) Criar nova senha\n(4) Ver senhas\n(5) Deletar\n(6) Atualizar Senha\n(7) Sair')

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

                pm.new_password(site, senha)
            case 4:
                pm.show_passwords()
            case 5:
                site = input('Nome do site: ')

                pm.delete_password(site)
            case 6:
                site = input('Site que deseja alterar a senha: ')
                senha = input('Nova senha: ')

                pm.update_password(site, senha)
            case 7:
                print('Saindo...')
                pm.sair_conta()
                break
            case _:
                print('Valor inválido')