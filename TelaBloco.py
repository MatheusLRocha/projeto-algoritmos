from tkinter import *

root = Tk()
global changer
changer = False # Variável global para controle de telas
root.overrideredirect(False) # Não brinque com isso (impede que a janela seja redimensionada, movida ou fechada)
root.title("PasSword") # Título da janela
root.iconphoto(True, PhotoImage(file="UNISAGRADO.png")) # Ícone da janela (precisa ser aberta como pasta para funcionar)
root.geometry("1200x700") # Dimensões da janela
root.resizable(False, False) # Impede a redimensionalização da janela
root.config(bg="#0c809f") # Cor de fundo da janela
