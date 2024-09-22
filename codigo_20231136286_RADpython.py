import sqlite3
from tkinter import *
from tkinter import messagebox

# Função para conectar ao banco de dados e criar a tabela
def connect_db():
    with sqlite3.connect('clientes.db') as conn:
        # Exclui a tabela antiga para recriar com a nova estrutura
        conn.execute('DROP TABLE IF EXISTS clientes')  # Apaga a tabela antiga, se houver

        conn.execute('''CREATE TABLE IF NOT EXISTS clientes 
                        (id INTEGER PRIMARY KEY, 
                         nome TEXT NOT NULL, 
                         telefone TEXT NOT NULL, 
                         idade INTEGER NOT NULL,
                         prontuario TEXT NOT NULL)''')

# Função para adicionar ou editar um cliente no banco de dados
def add_or_edit_cliente():
    nome = nome_entry.get()
    telefone = telefone_entry.get()
    idade = idade_entry.get()
    prontuario = prontuario_entry.get()

    if not (nome and telefone and idade and prontuario):
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    try:
        idade = int(idade)  # Verifica se a idade é um número
    except ValueError:
        messagebox.showerror("Erro", "Idade deve ser um número inteiro")
        return

    with sqlite3.connect('clientes.db') as conn:
        if selected_cliente.get() == -1:  # Adiciona novo cliente
            conn.execute("INSERT INTO clientes (nome, telefone, idade, prontuario) VALUES (?, ?, ?, ?)", 
                         (nome, telefone, idade, prontuario))
        else:  # Edita cliente existente
            conn.execute("UPDATE clientes SET nome=?, telefone=?, idade=?, prontuario=? WHERE id=?", 
                         (nome, telefone, idade, prontuario, selected_cliente.get()))

    clear_entries()
    view_clientes()

# Função para visualizar os clientes cadastrados
def view_clientes(search=""):
    listbox.delete(0, END)
    query = "SELECT * FROM clientes WHERE nome LIKE ?"
    with sqlite3.connect('clientes.db') as conn:
        for row in conn.execute(query, ('%' + search + '%',)):
            listbox.insert(END, row)

# Função para deletar um cliente pelo ID
def delete_cliente():
    try:
        selected = listbox.get(ACTIVE)
        with sqlite3.connect('clientes.db') as conn:
            conn.execute("DELETE FROM clientes WHERE id=?", (selected[0],))
        view_clientes()
    except IndexError:
        messagebox.showerror("Erro", "Selecione um cliente para deletar")

# Função para preencher os campos ao selecionar um cliente para editar
def select_cliente(event):
    try:
        selected = listbox.get(ACTIVE)
        selected_cliente.set(selected[0])

        nome_entry.delete(0, END)
        telefone_entry.delete(0, END)
        idade_entry.delete(0, END)
        prontuario_entry.delete(0, END)

        nome_entry.insert(END, selected[1])
        telefone_entry.insert(END, selected[2])
        idade_entry.insert(END, selected[3])
        prontuario_entry.insert(END, selected[4])
    except IndexError:
        pass

# Função para limpar os campos de entrada
def clear_entries():
    nome_entry.delete(0, END)
    telefone_entry.delete(0, END)
    idade_entry.delete(0, END)
    prontuario_entry.delete(0, END)
    selected_cliente.set(-1)

# Função principal para configurar a interface gráfica
def setup_gui(root):
    root.title("Gerenciador de Clientes")

    Label(root, text="Nome").grid(row=0, column=0)
    Label(root, text="Telefone").grid(row=1, column=0)
    Label(root, text="Idade").grid(row=2, column=0)
    Label(root, text="Prontuário").grid(row=3, column=0)

    global nome_entry, telefone_entry, idade_entry, prontuario_entry, listbox, selected_cliente, search_entry

    nome_entry = Entry(root)
    telefone_entry = Entry(root)
    idade_entry = Entry(root)
    prontuario_entry = Entry(root)
    search_entry = Entry(root)

    nome_entry.grid(row=0, column=1)
    telefone_entry.grid(row=1, column=1)
    idade_entry.grid(row=2, column=1)
    prontuario_entry.grid(row=3, column=1)

    Button(root, text="Salvar Cliente", command=add_or_edit_cliente).grid(row=4, column=1)
    Button(root, text="Deletar Cliente", command=delete_cliente).grid(row=4, column=0)
    Button(root, text="Limpar", command=clear_entries).grid(row=4, column=2)

    listbox = Listbox(root, width=50)
    listbox.grid(row=6, column=0, columnspan=3)
    listbox.bind('<<ListboxSelect>>', select_cliente)

    Label(root, text="Pesquisar").grid(row=5, column=0)
    search_entry.grid(row=5, column=1)
    Button(root, text="Buscar", command=lambda: view_clientes(search_entry.get())).grid(row=5, column=2)

# Início do programa
if __name__ == "__main__":
    root = Tk()
    selected_cliente = IntVar(root)  # Associa IntVar ao root e remove o argumento value=-1
    selected_cliente.set(-1)  # Agora você pode definir o valor inicial

    connect_db()

    setup_gui(root)
    view_clientes()
    root.mainloop()
