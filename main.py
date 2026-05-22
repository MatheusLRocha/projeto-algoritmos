# Arquivo que executa o projeto

# Importa uma única vez todas as bibliotecas e módulos que vão ser usados no projeto

from PasswordManager import PasswordService
from PasswordBank import PasswordRepository
from TelaBloqueio import TelaLogin

banco = PasswordRepository()
pm = PasswordService(banco)

if __name__ == '__main__':
    TelaLogin(pm)