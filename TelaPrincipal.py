from tkinter import *

root = Tk()
root.overrideredirect(False) # Não brinque com isso (impede que a janela seja redimensionada, movida ou fechada)
root.title("PasSword") # Título da janela
root.iconphoto(True, PhotoImage(file="UNISAGRADO.png")) # Ícone da janela (precisa ser aberta como pasta para funcionar)
root.geometry("1200x700") # Dimensões da janela
root.resizable(False, False) # Impede a redimensionalização da janela
root.config(bg="#0c809f") # Cor de fundo da janela


# Variáveis
global changer
changer = False # Variável global para controle de telas

titulo1 = "Unisagrado"
titulo2 = "Microsoft"
titulo3 = "Pergamum"
titulo4 = "Roblox"
titulo5 = "Netflix"

# Modelo de formatação

# Título
sample0 = {
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
sample1 = {
    "font":("Montserrat", 15, "bold"),
    "width":30,
    "height":20,
    "borderwidth":0,
    "fg":"#a8c7e4",
    "bg":"#141f29",
    "highlightbackground":"#141f29",
    "highlightcolor":"#141f29",
    "highlightthickness":12
}

# Botões
sample2 = {
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



# Funções
def change_bloco(num):
    mudar_bloco = Button(root,
                    text="Mudar bloco",
                    command=lambda: mudar_bloco(num))
    mudar_bloco.place(x=850, y=700)

def bloco_anotacao(num):
    if num == 0:
        # Cópia das Senhas para a área de transferência
        passwd = "123456"
        root.clipboard_clear() # Limpa a área de transferência
        root.clipboard_append(passwd) # Copia a senha para a área de transferência

        # Criação do campo de título da anotação
        titulo_bloco = Text(root,**sample0)
        titulo_bloco.place(x=850, y=0)
        titulo_bloco.insert(0.0, titulo1)

        # Criação do campo de anotação
        anotacao = Text(root,**sample1)
        anotacao.place(x=850, y=98)
        anotacao.insert(0.0, "Senha do e-mail da USC")
        change_bloco(num)

    elif num == 1:
        passwd = "batata"
        root.clipboard_clear() 
        root.clipboard_append(passwd) 

        titulo_bloco = Text(root,**sample0)
        titulo_bloco.place(x=850, y=0)
        titulo_bloco.insert(0.0, titulo2)

        anotacao = Text(root,**sample1)
        anotacao.place(x=850, y=98)
        anotacao.insert(0.0, "Senha do e-mail pessoal")
        change_bloco(num)

    elif num == 2:
        passwd = "valdomiro"
        root.clipboard_clear() 
        root.clipboard_append(passwd) 

        titulo_bloco = Text(root,**sample0)
        titulo_bloco.place(x=850, y=0)
        titulo_bloco.insert(0.0, titulo3)

        anotacao = Text(root,**sample1)
        anotacao.place(x=850, y=98)
        anotacao.insert(0.0, "Senha do Facebook")
        change_bloco(num)

    elif num == 3:
        passwd = "destruição"
        root.clipboard_clear() 
        root.clipboard_append(passwd) 

        titulo_bloco = Text(root,**sample0)
        titulo_bloco.place(x=850, y=0)
        titulo_bloco.insert(0.0, titulo4)

        anotacao = Text(root,**sample1)
        anotacao.place(x=850, y=98)
        anotacao.insert(0.0, "Sensd")
        change_bloco(num)

    elif num == 4:
        passwd = "bersek"
        root.clipboard_clear() 
        root.clipboard_append(passwd)

        titulo_bloco = Text(root,**sample0)
        titulo_bloco.place(x=850, y=0)
        titulo_bloco.insert(0.0, titulo5)

        anotacao = Text(root,**sample1)
        anotacao.place(x=850, y=98)
        anotacao.insert(0.0, "Senha da senha")
        change_bloco(num)
        









# Blocos botões

bloco1 = Button(root,
            text=titulo1,
            **sample2,
            command=lambda: bloco_anotacao(0))

bloco2 = Button(root,
            text=titulo2,
            **sample2,
            command=lambda: bloco_anotacao(1))

bloco3 = Button(root,
            text=titulo3,
            **sample2,
            command=lambda: bloco_anotacao(2))

bloco4 = Button(root,
            text=titulo4,
            **sample2,
            command=lambda: bloco_anotacao(3))

bloco5 = Button(root,
            text=titulo5,
            **sample2,
            command=lambda: bloco_anotacao(4))


# Posicionamento dos blocos

bloco1.place(x=120, y=50)
bloco2.place(x=120, y=200)
bloco3.place(x=120, y=350)
bloco4.place(x=120, y=500)
bloco5.place(x=120, y=650)



root.mainloop()
