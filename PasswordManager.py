from PasswordBank import PasswordRepository
import base64 # Mexe com codificação e decodificação de dados
import os # Mexe com arquivos e diretórios
from cryptography.fernet import Fernet, InvalidToken # Criptografia simétrica, cria uma chave para descriptografar e criptografar dados
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id # Derivação de chaves(KDF)
import random # biblioteca para aleatorizar os valores para senha aleatória
from time import sleep # sleep permite criar um temporizador entre as tentativas de login. Serve para atrasar em caso de brute force
from peewee import OperationalError, DoesNotExist # Validações de erros da biblioteca peewee

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
    def create_account(self, passphrase):
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

        print('Conta criada com sucesso!')

        # Após criar a conta, o usuário já está logado
        self.isLogged = True

    # Verifica se o usuário tem uma conta
    def login_account(self, master_password):
        try:
            # Pega o salt armazenado
            with open('salt.txt', 'rb') as f:
                salt = f.read()
        except FileNotFoundError:
            print('Arquivo de salt não encontrado')
            self.isLogged = False
        else:
            try:
                # Pega a autenticação criptografada armazenada
                with open('autenticacao.txt', 'rb') as f:
                    encrypted_data = f.readline()
            except FileNotFoundError:
                print('Arquivo de autenticação não encontrado')
                self.isLogged = False
            else:
                # Verifica se a senha está correta
                try:
                    # Gera a chave de criptografia a partir da senha mestre e do salt, e coloca ela no fernet
                    key = self.generate_key(master_password, salt)
                    self.fernet = Fernet(key)

                    # Descriptografa a autenticação para verificar se a senha mestre está correta
                    self.fernet.decrypt(encrypted_data)
                except InvalidToken: 
                    # InvalidToken ocorre quando ao tentar gerar a chave e abrir o cofre, o valor passado não é o mesmo que foi usado para criá-la
                    print('Chave inválida, erro ao tentar descriptografar com a senha passada!')
                    sleep(3) # Temporizador de 3 segundos
                    print('Login negado')
                    
                    self.isLogged = False
                else:
                    print('Login feito com sucesso!')

                    self.isLogged = True
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
        if self.isLogged:
            try:
                encrypted_passwords = self.banco.list()
                return encrypted_passwords
            except OperationalError:
                print('Ainda não há uma tabela ou banco criados.')
        else:
            print('Você não possui acesso, verifique seu login')

    def update_password(self, id, new_password):
        if self.isLogged:
            try:
                encrypted_new_password = self.fernet.encrypt(new_password.encode())
                
                self.banco.update(id, encrypted_new_password.decode()) # podemos atulizar a criptografia do titulo também(opcional)
            except DoesNotExist:
                print('Consulta não encontrada no banco de dados')
        else:
            print('Você não possui acesso, verifique seu login')
    
    def delete_password(self, id):
        if self.isLogged:
            try:
                self.banco.delete(id)
            except DoesNotExist:
                print('Consulta não encontrada no banco de dados')
        else:
            print('Você não possui acesso, verifique seu login')

    def random_password(self):
        # Existe um jeito melhor utilizando uma biblioteca, mas aqui por enquanto fica no modo manual
        lowercase_caracters = 'abcdefghijklmnopqrstuvwxyz'
        uppercase_caracters = lowercase_caracters.upper()
        special_caracters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        numbers = '0123456789'

        all_caracters = lowercase_caracters + uppercase_caracters + special_caracters + numbers

        # join() permite juntar todos os itens de um iterável e juntá-los em uma string
        rpassword = ''.join(random.choices(all_caracters, k=20))

        return rpassword
        



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