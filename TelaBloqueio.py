from tkinter import *
from PasswordBank import Authentication

def TelaLogin(pm, user_register=False):

        root = Tk() # Base TkInter
        root.overrideredirect(False) # Não brinque com isso (impede que a janela seja redimensionada, movida ou fechada)
        root.title("PasSword") # Título da janela
        root.iconphoto(True, PhotoImage(file="UNISAGRADO.png")) # Ícone da janela (precisa ser aberta como pasta para funcionar)
        root.geometry("600x800") # Dimensões da janela
        root.resizable(False, False) # Impede a redimensionalização da janela
        root.config(bg="#0c809f") # Cor de fundo da janela

        # Textos
        preSword = Label(root,
                        text="Corte todos os riscos de roubo de senhas com o", # Texto do subtítulo
                        font=("Montserrat",15,"bold"), # Fonte, tamanho da fonte e estilo do subtítulo
                        bg="#0c809f")
        preSword.place(x=65,y=30) # Posicionamento do subtítulo


        pasSword = Label(root,
                        text="PasSword!",
                        font=("Montserrat",60,"underline","bold"),
                        fg="#a8c7e4", # Cor do título
                        bg="#0c809f")
        pasSword.place(x=90,y=100) # Posicionamento do título


        # .exists() retorna True se já houver uma linha de autenticação salva na tabela
        isUser = Authentication.select().exists()
        new_register = user_register

        if isUser == True and new_register == False:
            passw = Label(root,
                        text="Senha",
                        font=("Montserrat",22,"bold"),
                        bg="#0c809f")
            passw.place(x=245,y=400) # Posicionamento do texto do campo de senha

            # Campos de entrada

            user_passw = Entry(root,
                            font=("Montserrat",20),
                            width=30,
                            borderwidth=2,
                            show="*") # Esconde o texto digitado com asteriscos
            user_passw.place(x=70,y=450) # Posicionamento do campo de entrada para a senha


            # Funções
            def login():

                if pm.login_account(user_passw.get()): # Verifica se o usuário e a senha estão corretos (nesse caso, ambos são "admin")
                    root.destroy() # Fecha a janela atual

                    import TelaPrincipal # Importa o arquivo da tela principal (precisa ser aberta como pasta para funcionar)
                    TelaPrincipal.abrir_tela(pm)

                else:
                    user_passw.delete(0, END) # Limpa o campo de entrada da senha
                    user_passw.focus() # Foca no campo de entrada do usuário
                    error = Label(root,
                                text="Senha incorreta!", # Texto do erro
                                font=("Montserrat",20,"bold"),
                                fg="#990c0c", # Cor do texto do erro
                                bg="#0c809f")
                    error.place(x=190,y=500) # Posicionamento do texto de erro

            def new_login():
                new_register = True
                root.destroy()
                TelaLogin(pm, new_register)

            def sure():
                sure = Tk()
                sure.title("Tem certeza?") # Título da janela
                sure.geometry("600x200") # Dimensões da janela
                sure.resizable(False, False) # Impede a redimensionalização da janela
                sure.config(bg="#a8c7e4") # Cor de fundo da janela
                sure_label = Label(sure,
                                text="Tem certeza que deseja criar outro usuário?\nIsso apagará todos os seus dados atuais...", # Texto do erro
                                font=("Montserrat",20,"bold"),
                                fg="#990c0c", # Cor do texto do erro
                                bg="#a8c7e4")
                sure_label.pack(pady=10) # Posicionamento do texto de erro


                new_login_button = Button(sure,
                                text="Sim",
                                font=("Montserrat",26,"bold"),
                                bg="#990c0c",
                                fg="#a8c7e4",
                                borderwidth=2,
                                command=new_login)
                new_login_button.pack(pady=10) # Posicionamento do botão de login
            
            # Botões
            login_button = Button(root,
                                text="Login",
                                font=("Montserrat",20,"bold"),
                                bg="#a8c7e4",
                                fg="#0c809f",
                                borderwidth=2,
                                command=login)
            login_button.place(x=245,y=570) # Posicionamento do botão de login


            sure_new_button = Button(root,
                                text="Novo usuário",
                                font=("Montserrat",20,"bold"),
                                bg="#a8c7e4",
                                fg="#990c0c",
                                borderwidth=2,
                                command=sure)
            sure_new_button.place(x=197,y=680) # Posicionamento do botão de login

        else:
            # Texto da nova senha
            newpassw = Label(root,
                        text="Cadastre-se!\nDigite sua nova senha \n(e não se esqueça dela!)",
                        font=("Montserrat",28,"bold"),
                        bg="#0c809f")
            newpassw.place(x=80,y=290) # Posicionamento do texto do campo de senha


            # Entrada da nova senha
            user_newpassw = Entry(root,
                            font=("Montserrat",24),
                            width=25,
                            borderwidth=2) # Esconde o texto digitado com asteriscos
            user_newpassw.place(x=72,y=450) # Posicionamento do campo de entrada para a senha


            # Função de primeiro login
            def signup():
                pm.create_account(user_newpassw.get())
                root.destroy() # Fecha a janela atual

                import TelaPrincipal # Importa o arquivo da tela principal (precisa ser aberta como pasta para funcionar)
                TelaPrincipal.abrir_tela(pm)



            # Botão de criar conta
            signup_button = Button(root,
                                text="Criar conta local",
                                font=("Montserrat",30,"bold"),
                                bg="#a8c7e4",
                                fg="#0c809f",
                                borderwidth=2,
                                command=signup)
            signup_button.place(x=125,y=600) # Posicionamento do botão de login




        root.mainloop()