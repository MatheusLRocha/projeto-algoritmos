from tkinter import *
from TelaBloco import open_window

def abrir_tela(pm):
    root = Tk()
    root.overrideredirect(False)  # Não brinque com isso
    root.title("PasSword")
    root.iconphoto(True, PhotoImage(file="UNISAGRADO.png"))
    root.geometry("1200x700")
    root.resizable(False, False)
    root.config(bg="#0c809f")


    # Modelos de formatação dos textos usados

    sampleh1 = {
        "font": ("Montserrat", 24, "bold"),
        "width": 24,
        "height": 2,
        "borderwidth": 0,
        "fg": "#0c809f",
        "bg": "#141f29",
        "highlightbackground": "#141f29",
        "highlightcolor": "#141f29",
        "highlightthickness": 30,
    }

    sampleh2 = {
        "font": ("Montserrat", 15, "bold"),
        "width": 38,
        "height": 18,
        "borderwidth": 0,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "highlightbackground": "#141f29",
        "highlightcolor": "#141f29",
        "highlightthickness": 12,
    }

    samplebutton = {
        "font": ("Montserrat", 20, "bold"),
        "width": 35,
        "height": 2,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "activebackground": "#141f29",
        "activeforeground": "#a8c7e4",
        "bd": 0,
        "highlightcolor": "#a8c7e4",
    }

    samplebuttonplus = {
        "font": ("Montserrat", 22, "bold"),
        "width": 34,
        "height": 1,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "activebackground": "#141f29",
        "activeforeground": "#a8c7e4",
        "bd": 0,
        "highlightcolor": "#a8c7e4",
    }

    samplebuttonedit = {
        "font": ("Montserrat", 11, "bold"),
        "width": 25,
        "height": 1,
        "fg": "#a8c7e4",
        "bg": "#141f29",
        "activebackground": "#141f29",
        "activeforeground": "#a8c7e4",
        "bd": 5,
        "highlightcolor": None,
    }


    # Configuração do Canvas e Frames para Scrollbar funcional dos blocos
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Frame base para a divisão da tela principal em frame esquerdo e direito
    main_frame = Frame(root, bg="#0c809f")
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=0)

    # Frame esquerdo responsável pelo Scrollbar e a funcionalidade dos blocos a partir do Canvas
    left_frame = Frame(main_frame, bg="#0c809f")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=5)
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    canvas = Canvas(left_frame, bg="#0c809f", highlightthickness=0)
    scrollbar = Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew", padx=(0,20))
    scrollbar.grid(row=0, column=1, sticky="ns")

    cards_frame = Frame(canvas, bg="#0c809f")
    frame_window = canvas.create_window((0, 0), window=cards_frame, anchor="nw")

    def atualizar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajustar_largura_frame(event):
        canvas.itemconfigure(frame_window, width=event.width)

    cards_frame.bind("<Configure>", atualizar_scroll)
    canvas.bind("<Configure>", ajustar_largura_frame)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    cards_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    cards_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))



    # Frame direito para a descrição dos blocos
    right_frame = Frame(main_frame, bg="#0c809f")
    right_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
    right_frame.grid_rowconfigure(2, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    detail_label = Label(
        right_frame,
        text="Detalhes do bloco",
        fg="#a8c7e4",
        bg="#0c809f",
        font=("Montserrat", 18, "bold"),
    )
    detail_label.grid(row=0, column=0, sticky="w", pady=(0, 10), padx=(20,0))

    titulo_bloco = Text(right_frame, **sampleh1)
    titulo_bloco.grid(row=1, column=0, sticky="ew", padx=(20,0))

    anotacao = Text(right_frame, **sampleh2)
    anotacao.grid(row=2, column=0, sticky="nsew", pady=(10, 0), padx=(20,0))

    def add_card():
        root.destroy()
        open_window(None, pm, None, None, lambda: abrir_tela(pm))

    def change_card(id, title, password):
        root.destroy()
        open_window(id, pm, title, password, lambda: abrir_tela(pm))

    def mostrar_detalhe(title, encrypted_password):
        senha = pm.fernet.decrypt(encrypted_password.encode()).decode()
        root.clipboard_clear()
        root.clipboard_append(senha)
        titulo_bloco.delete("1.0", "end")
        titulo_bloco.insert("1.0", title)
        anotacao.delete("1.0", "end")
        anotacao.insert("1.0", senha)


    # Bloco que adiciona novos blocos de senha
    add_card_block = Button(
        cards_frame,
        text="+",
        **samplebuttonplus,
        command=add_card,
    )
    add_card_block.grid(row=0, column=0,columnspan=5, padx=0, pady=20)


    # Sequência que insere blocos na tela por cada senha contida no banco de dados
    card_row = 1

    def card(id, title, password):
        nonlocal card_row
        row_frame = Frame(cards_frame, bg="#0c809f")
        row_frame.grid(row=card_row, column=0, sticky="ew", padx=20, pady=10)
        row_frame.grid_columnconfigure(1, weight=2)

        edit_block = Button(
            row_frame,
            text=">",
            **samplebuttonedit,
            command=lambda: change_card(id, title, password),
        )
        edit_block.grid(row=1, column=1, padx=(0,0), sticky="e")

        card_anotacao = Button(
            row_frame,
            text=title,
            **samplebutton,
            command=lambda: mostrar_detalhe(title, password),
        )
        card_anotacao.grid(row=0, column=1, sticky="ew")

        delete_card_block = Button(
            row_frame,
            text="-",
            **samplebuttonedit,
            command=lambda: delete_card(id),
        )
        delete_card_block.grid(row=1, column=1, padx=0, sticky="w")

        card_row += 1

    def delete_card(id):
        pm.delete_password(id)
        root.destroy()
        abrir_tela(pm)

    encrypted_passwords = pm.show_passwords()

    if encrypted_passwords is not None:
        for item in encrypted_passwords:
            title = item.title
            encrypted_password = item.password
            decrypt_title = pm.fernet.decrypt(title.encode()).decode()
            card(item.id, decrypt_title, encrypted_password)

    root.mainloop()
