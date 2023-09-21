# importando SQLite
import random
import sqlite3
import sqlite3 as lite
import pandas as pd
import io
from sqlite3 import Error
from tkinter import filedialog, messagebox, simpledialog

# Criando conexão
con = lite.connect('dados.db')

# Funções para inserções

# Inserir categorias
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query,i)

# Inserir Receitas
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em, valor) VALUES (?,?,?)"
        cur.execute(query,i)

# Inserir Gastos
def inserir_gasto(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query,i)

# Funções para deletar

# Deletar Categoria
def deletar_categoria(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Categoria WHERE id=?"
        cur.execute(query, i)

# Deletar Receitas
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

# Deletar Gastos
def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

# Deletar todas receitas e gastos
'''
def deletar_tudo():
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE *"
        cur.execute(query)
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE *"
        cur.execute(query)
'''

# Funções para ver dados

# Ver categorias
def ver_categoria():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver receitas
def ver_receitas():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver gastos
def ver_gastos():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# função para dados da tabela
def tabela():
    gastos = ver_gastos()
    receita = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receita:
        tabela_lista.append(i)

    return tabela_lista

# função para dados do grafico de barras
def bar_valores():
    # receita total
    receitas = ver_receitas()
    receita_lista = []

    for i in receitas:
        receita_lista.append(i[3])

    receita_total = sum(receita_lista)

    # despesa total
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])

    gastos_total = sum(gastos_lista)

    # Saldo total
    saldo_total = receita_total - gastos_total

    return[receita_total, gastos_total, saldo_total]

# função grafico pie
def pie_valores():
    gastos = ver_gastos()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns = ['id','Categoria','Data','Valor'])
    dataframe = dataframe.groupby('Categoria')['Valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias, lista_quantias])

# função para valor porcentagem
def porcentagem_valor():
    # Receita total
    receita = ver_receitas()
    receitas_lista = []

    for i in receita:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # Despesa total
    despesa = ver_gastos()
    despesa_lista = []

    for i in despesa:
        despesa_lista.append(i[3])

    despesa_total = sum(despesa_lista)

    # Porcentagem

    if receita_total == 0:
        pass
    else:
        total = (despesa_total/receita_total)*100
        return(total)
    
# Backup
def backup():
    nome_arquivo = filedialog.asksaveasfilename()
    con = sqlite3.connect('dados.db')
    # Open() function 
    with io.open(nome_arquivo+'.sql', 'w') as p: 
            
        # iterdump() function
        for line in con.iterdump(): 
            
            p.write('%s\n' % line)

    con.close()
        
    messagebox.showinfo('Sucesso','Salvo com sucesso!')
    
# Restaurando Backup
def rec_backup():
    arquivo = filedialog.askopenfile(mode='r')
    con = sqlite3.connect('dados.db')
    cursor = con.cursor()
    #f = io.open(arquivo,'r')
    #sql = f.read()
    sql = arquivo.read()
    cursor.executescript(sql)
    
    con = sqlite3.connect('dados.db')

    con.close()

    messagebox.showinfo('Sucesso','Informações carregadas com sucesso!')