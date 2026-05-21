from tkinter import *
from tkinter import ttk

def open_window(id, on_close=None):
    root = Tk()
    root.overrideredirect(False) # Não brinque com isso (impede que a janela seja redimensionada, movida ou fechada)
    root.title("PasSword") # Título da janela
    root.iconphoto(True, PhotoImage(file="UNISAGRADO.png")) # Ícone da janela (precisa ser aberta como pasta para funcionar)
    root.geometry("1200x700") # Dimensões da janela
    root.resizable(False, False) # Impede a redimensionalização da janela
    root.config(bg="#141f29") # Cor de fundo da janela


    # Modelos
    sampleh1= {"bg": "#141f29",
                "fg": "#a8c7e4",
                "font": ("Montserrat", 24, "bold"),
                "bd": 0,
                "width": 10,
                "height": 1,
        }

    sampleh2= {"bg": "#141f29",
                "fg": "#a8c7e4",
                "font": ("Montserrat", 22, "bold"),
                "bd": 0,
                "width": 20,
                "height": 1,
        }

    sampletext = {
                "font":("Montserrat", 26, "bold"),
                "width":40,
                "height":1,
                "borderwidth":0,
                "fg":"#a8c7e4",
                "bg":"#141f29",
                "highlightbackground":"#141f29",
                "highlightcolor":"#141f29",
                "highlightthickness":0
            }

    sampletext2 = {
                "font":("Montserrat", 28, "bold"),
                "width":40,
                "height":7,
                "borderwidth":0,
                "fg":"#70b3f1",
                "bg":"#141f29",
                "highlightbackground":"#141f29",
                "highlightcolor":"#141f29",
                "highlightthickness":0
            }
    
    samplebutton = {
                "font": ("Montserrat", 20, "bold"),
                "bg": "#141f29",
                "fg": "#a8c7e4",
                "bd": 0,
                "width": 10,
                "height": 1,
            }
    if (id==None):

        # Titulos
        new_title = Label(text="Título:",
                            **sampleh1)
        new_title.place(x=30, y=50)
        # Título criado
        new_block_title = Text(**sampletext)
        new_block_title.place(x=220, y=50)


        # Separador 1
        sep1 = ttk.Separator(root, orient="horizontal")
        sep1.place(x=0, y=145, width=1200)


        # Senhas
        new_passwd = Label(text="Senha:",
                        **sampleh1)
        new_passwd.place(x=50, y=190)
        # Senha criada
        new_block_passwd = Text(**sampletext)
        new_block_passwd.place(x=240, y=190)


        # Botão gerador de senhas
        new_generated = Button(text="Gerar senha aleatória",
                            **sampleh2)
        new_generated.place(x=150, y=270)


        # Separador 2
        sep2 = ttk.Separator(root, orient="horizontal")
        sep2.place(x=0, y=350, width=1200)


        # Notas
        new_notes = Label(text="Notas:",
                        **sampleh1)
        new_notes.place(x=50, y=380)
        # Notas criadas
        new_block_notes = Text(**sampletext2)
        new_block_notes.place(x=240, y=382)

    else:

        # Titulos
        new_title = Label(text="Título:",
                            **sampleh1)
        new_title.place(x=30, y=50)
        # Título criado
        new_block_title = Text(**sampletext2)
        new_block_title.insert("1.0",f"Título pré-selecionado do bloco id{id}")
        new_block_title.place(x=220, y=50)


        # Separador 1
        sep1 = ttk.Separator(root, orient="horizontal")
        sep1.place(x=0, y=145, width=1200)


        # Senhas
        new_passwd = Label(text="Senha:",
                        **sampleh1)
        new_passwd.place(x=50, y=190)
        # Senha criada
        new_block_passwd = Text(**sampletext2)
        new_block_passwd.insert("1.0",f"Senha pré-selecionada do bloco id{id}")
        new_block_passwd.place(x=240, y=190)


        # Botão gerador de senhas
        new_generated = Button(text="Gerar senha aleatória",
                            **sampleh2)
        new_generated.place(x=150, y=270)


        # Separador 2
        sep2 = ttk.Separator(root, orient="horizontal")
        sep2.place(x=0, y=350, width=1200)


        # Notas
        new_notes = Label(text="Notas:",
                        **sampleh1)
        new_notes.place(x=50, y=380)
        # Notas criadas
        new_block_notes = Text(**sampletext2)
        new_block_notes.insert("1.0",f"Anotações pré-selecionadas do bloco {id}")
        new_block_notes.place(x=240, y=382)

    # Função alteradora de mudanças e volta para a tela principal
    def accept_changes(id=None):
            variavel_titulo = new_block_title.get("1.0", "end-1c")
            variavel_senha = new_block_passwd.get("1.0", "end-1c")
            variavel_notas = new_block_notes.get("1.0", "end-1c")
            root.destroy()
            if callable(on_close):
                try:
                    on_close()
                except Exception:
                    pass

    # Botão de alterar mudanças
    accept_changes_button = Button(root,
                                text="Alterar bloco",
                                **samplebutton,
                                command=lambda id=id: accept_changes(id))
    accept_changes_button.place(x=25, y=600)
    
    
    