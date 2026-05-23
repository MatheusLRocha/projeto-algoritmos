from tkinter import *
from TelaBloco import open_window

def abrir_tela(pm):
    root = Tk()
    root.overrideredirect(False) # Não brinque com isso (impede que a janela seja redimensionada, movida ou fechada)
    root.title("PasSword") # Título da janela
    root.iconphoto(True, PhotoImage(file="UNISAGRADO.png")) # Ícone da janela (precisa ser aberta como pasta para funcionar)
    root.geometry("1200x700") # Dimensões da janela
    root.resizable(False, False) # Impede a redimensionalização da janela
    root.config(bg="#0c809f") # Cor de fundo da janela

    # Variáveis

    # Modelo de formatação

    # Título
    sampleh1 = {
        "font":("Montserrat", 24, "bold"),
        "width":16,
        "height":2,
        "borderwidth":0,
        "fg":"#0c809f",
        "bg":"#141f29",
        "highlightbackground":"#141f29",
        "highlightcolor":"#141f29",
        "highlightthickness":30
    }

    # Anotação
    sampleh2 = {
        "font":("Montserrat", 15, "bold"),
        "width":30,
        "height":30,
        "borderwidth":0,
        "fg":"#a8c7e4",
        "bg":"#141f29",
        "highlightbackground":"#141f29",
        "highlightcolor":"#141f29",
        "highlightthickness":12
    }

    # Botões
    samplebutton = {
        "font": ("Montserrat", 20, "bold"),
        "width": 40,
        "height": 2,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "activebackground": "#141f29",
        "activeforeground": "#a8c7e4",
        "bd": 0,
        "highlightcolor": "#a8c7e4"
    }

    samplebuttonplus = {
        "font": ("Montserrat", 22, "bold"),
        "width": 37,
        "height": 1,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "activebackground": "#141f29",
        "activeforeground": "#a8c7e4",
        "bd": 0,
        "highlightcolor": "#a8c7e4"
    }

    samplebuttonedit = {
        "font": ("Montserrat", 11, "bold"),
        "width": 3,
        "height": 1,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "activebackground": "#141f29",
        "activeforeground": "#a8c7e4",
        "bd": 5,
        "highlightcolor": None
    }





    # Slider lateral

    slider = Scale(root, 
                from_=100, 
                to=0, 
                orient=VERTICAL, 
                length=700, 
                width=15,
                showvalue=0, 
                sliderlength=30, 
                troughcolor="#141f29", 
                fg="#141f29", 
                bg="#a8c7e4",
                bd=0,
                highlightcolor="#a8c7e4", 
                font=("Montserrat", 12, "bold"))
    slider.set(slider['from'])
    slider.pack(side=LEFT)



    # Ativa o botão de adicionar um novo bloco
    def add_card():
        root.destroy() # Fecha a janela atual
        open_window(None, pm, None, None, lambda: abrir_tela(pm))# Importa o arquivo da tela principal (precisa ser aberta como pasta para funcionar)

    
    
    # Ativa o botão de alterar um bloco
    def change_card(id, title, password):
        root.destroy()
        open_window(id, pm, title, password, lambda: abrir_tela(pm))


    # Modelo instanciável dos blocos
    def notepad(title, encrypted_password):
        senha = pm.fernet.decrypt(encrypted_password.encode()).decode()

        # Cópia das Senhas para a área de transferência
        passwd = senha
        root.clipboard_clear() # Limpa a área de transferência
        root.clipboard_append(passwd) # Copia a senha para a senhas = GerenciadorDeSenhas.ver_senhas()área de transferência
        # root.after(15000, lambda:root.clipboard_clear()) # Limpa o clipboard após 15 segundos, tornando mais seguro contra outros apps lerem ele

        # Criação do campo de título da anotação
        titulo_bloco = Text(root,**sampleh1)
        titulo_bloco.place(x=850, y=0)
        titulo_bloco.insert(0.0, title)

        # Criação do campo de anotação
        anotacao = Text(root,**sampleh2)
        anotacao.place(x=850, y=98)
        anotacao.insert(0.0, passwd)
        


    # Botão de adicionar um bloco
    add_card_block = Button(root,
                            text="+",
                            **samplebuttonplus,
                            command=add_card)
    add_card_block.place(x=125, y=10)


    # Instancia todas as senhas presentes
    def card(id, title, password):
        card_anotacao = Button(root,
                            text=title,
                            **samplebutton,
                            command=lambda: notepad(title, password))
        thispace = 100 + space
        card_anotacao.place(x=120, y=thispace)
        # Botão editar bloco
        edit_block = Button(root,text=">",
                    **samplebuttonedit,
                    command=lambda:change_card(id, title, password))
        edit_block.place(x=45, y=thispace)
        
        
        # Função de deletar
        def delete_card(id):
            pm.delete_password(id)

            # Destroi a janela e recria ela(mudar para uma função melhor do que isso se tiver)
            root.destroy()
            abrir_tela(pm)
            
        # Bloco de deletar
        delete_card_block = Button(root,
                                text="-",
                                **samplebuttonedit,
                                command=lambda:delete_card(id))
        delete_card_block.place(x=45, y=thispace+50)



    # Prepara a instanciação das senhas
    encrypted_passwords = pm.show_passwords()
    space=0

    if encrypted_passwords is not None:
        for item in encrypted_passwords:
            title = item.title
            encrypted_password = item.password

            decrypt_title = pm.fernet.decrypt(title.encode()).decode()

            card(item.id, decrypt_title, encrypted_password)
            space+=130

    root.mainloop()