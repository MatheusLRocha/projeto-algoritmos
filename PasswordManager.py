from PasswordBank import PasswordRepository, Authentication
import base64 # Mexe com codificação e decodificação de dados
import os # Mexe com arquivos e diretórios
from cryptography.fernet import Fernet, InvalidToken # Criptografia simétrica, cria uma chave para descriptografar e criptografar dados
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id # Derivação de chaves(KDF)
from time import sleep # sleep permite criar um temporizador entre as tentativas de login. Serve para atrasar em caso de brute force
from peewee import OperationalError, DoesNotExist # Validações de erros da biblioteca peewee
import secrets # Biblioteca para aleatorizar os valores para senha aleatória segura(Melhor para criptografia que o random)
import string # Biblioteca de string para capturar letras, números e símbolos de forma mais fácil

class PasswordService:
    # Criação do constructor
    def __init__(self, banco):
        self.banco = banco
        self.isLogged = False
        self.fernet = None
        
    # Gera chave de criptografia com base na senha mestre e salt.    
    def generate_key(self, master_password: str, salt: bytes):
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
        salt = os.urandom(16) # urandom gera bytes aleatórios para criptografia

        # Gera a chave e criptografia e coloca ela no fernet
        key = self.generate_key(passphrase, salt)
        self.fernet = Fernet(key)

        # Gera um token de autenticação aleatório para verificar usuário
        safe_token = self.fernet.encrypt(secrets.token_bytes(32)).decode()

        try:
            # Apaga qualquer configuração de autenticação antiga se existir e...
            self.banco.new_auth(salt, safe_token) # Cria no banco o registro do salt e do token de segurança já criptografados

            # Deleta as senhas da conta antiga e cria uma nova tabela de senhas
            self.banco.new_register()

            print("Conta criada com sucesso")

            self.isLogged = True
        except OperationalError:
            print("Erro ao acessar o banco de dados")

    # Verifica se o usuário tem uma conta
    def login_account(self, master_password):
        try:
            # Busca o registro de configuração salvo na tabela de Autenticação
            auth_settings = Authentication.get()

            # Pega salt armazenado no registro
            salt = bytes(auth_settings.salt)

            # Pega o token de autenticação armazenado no registro
            encrypted_data = auth_settings.auth 
        except DoesNotExist:
            print("Nenhuma conta configurada encontrada")
            self.isLogged = False
        except OperationalError:
            print("Erro ao ler a tabela de Autenticação")
            self.isLogged = False
        else:
            try:
                # Gera a chave de criptografia a partir da senha mestre e do salt, e coloca ela no fernet
                key = self.generate_key(master_password, salt)
                self.fernet = Fernet(key)

                # Tenta descriptografar a autenticação para verificar se a senha mestre está correta
                self.fernet.decrypt(encrypted_data.encode())
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
        chars = string.ascii_letters + string.digits + string.punctuation

        # join() permite juntar todos os itens de um iterável e juntá-los em uma string
        rpassword = ''.join(secrets.choice(chars) for _ in range(20))

        return rpassword