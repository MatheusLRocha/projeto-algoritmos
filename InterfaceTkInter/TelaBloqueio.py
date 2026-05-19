from tkinter import *
from PIL import Image, ImageTk
import main

root = Tk() # Base TkInter
global changer
changer = False # Variável global para controle de telas
root.overrideredirect(False) # Não brinque com isso (impede que a janela seja redimensionada, movida ou fechada)
root.title("PasSword") # Título da janela
root.iconphoto(True, PhotoImage(file="UNISAGRADO.png")) # Ícone da janela (precisa ser aberta como pasta para funcionar)
root.geometry("600x800") # Dimensões da janela
root.resizable(False, False) # Impede a redimensionalização da janela
root.config(bg="#0c809f") # Cor de fundo da janela

# Instancia o gerenciador de senhas para acessar as funções de login e gerenciamento de senhas
pm = main.GerenciadorDeSenhas()

# Tela Login

# Funções
def login():
    
    global changer
    if user_login.get() == "admin" and user_passw.get() == "admin": # Verifica se o usuário e a senha estão corretos (nesse caso, ambos são "admin")
        changer = True # Altera a variável global "changer" para 1 para mostrar a tela principal
        root.destroy() # Fecha a janela atual
        import TelaPrincipal # Importa o arquivo da tela principal (precisa ser aberta como pasta para funcionar)
    else:
        user_login.delete(0, END) # Limpa o campo de entrada do usuário
        user_passw.delete(0, END) # Limpa o campo de entrada da senha
        user_login.focus() # Foca no campo de entrada do usuário
        error = Label(root,
                    text="Usuário ou senha incorretos!", # Texto do erro
                    font=("Montserrat",15,"bold"),
                    fg="#990c0c", # Cor do texto do erro
                    bg="#0c809f")
        error.place(x=150,y=750) # Posicionamento do texto de erro








# Textos
preSword = Label(root,
                text="Corte todos os riscos de roubo de senhas com o", # Texto do subtítulo
                font=("Montserrat",15,"bold"), # Fonte, tamanho da fonte e estilo do subtítulo
                bg="#0c809f")
pasSword = Label(root,
                text="PasSword!",
                font=("Montserrat",60,"underline","bold"),
                fg="#a8c7e4", # Cor do título
                bg="#0c809f")
user = Label(root,
            text="Usuário",
            font=("Montserrat",22,"bold"),
            bg="#0c809f")
passw = Label(root,
            text="Senha",
            font=("Montserrat",22,"bold"),
            bg="#0c809f")


# Campos de entrada
user_login = Entry(root,
                font=("Montserrat",20),
                width=30, # Largura do campo de entrada
                borderwidth=2) # Largura da borda
user_passw = Entry(root,
                font=("Montserrat",20),
                width=30,
                borderwidth=2,
                show="*") # Esconde o texto digitado com asteriscos



# Botões
login_button = Button(root,
                    text="Login",
                    font=("Montserrat",20,"bold"),
                    bg="#a8c7e4",
                    fg="#0c809f",
                    borderwidth=2,
                    command=login)


# Posicionamento dos elementos
preSword.place(x=65,y=30) # Posicionamento do subtítulo
pasSword.place(x=90,y=100) # Posicionamento do título

user.place(x=245,y=340) # Posicionamento do texto do campo de usuário
passw.place(x=256,y=510) # Posicionamento do texto do campo de senha

user_login.place(x=85,y=390) # Posicionamento do campo de entrada para o usuário
user_passw.place(x=85,y=560) # Posicionamento do campo de entrada para a senha

login_button.place(x=250,y=690) # Posicionamento do botão de login





root.mainloop()