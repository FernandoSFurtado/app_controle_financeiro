from logging import root
from multiprocessing import parent_process, process
from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date

# Importando funções da view
from view import backup, rec_backup, deletar_categoria, porcentagem_valor, pie_valores, bar_valores, tabela, inserir_categoria, inserir_receita, inserir_gasto, deletar_receitas, deletar_gastos, ver_categoria, ver_receitas, ver_gastos

# cores 
co0 = "#2e2d2b"  
co1 = "#feffff"  
co2 = "#4fa882"  
co3 = "#38576b"  
co4 = "#403d3d"   
co5 = "#e06636"   
co6 = "#038cfc"   
co7 = "#3fbfb9"   
co8 = "#263238"   
co9 = "#e9edf5"   

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# Criando janela

janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

# Criando frames para divisão da tela

frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0,column=0)

frameMeio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_pie = Frame(frameMeio, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)

frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0, column=2, padx=5)

# Trabalhando no frameCima

# Acessando imagem

app_img = Image.open('img/money.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" Orçamento pessoal", width=900, compound=LEFT,
                  padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0, y=0)

# Botão Backup



# Botão Restaurar



# Definindo tree como global

global tree

# Função inserir categoria

def inserir_categoria_b():
    nome = e_categoria.get()
    
    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
        
    # passando para a função inserir gastos presentes na view    
    inserir_categoria(lista_inserir)

    messagebox.showinfo('Sucesso','Dados inseridos com sucesso')

    e_categoria.delete(0,'end')

    # Pegando os valores da categoria 
    categorias_funcao = ver_categoria()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

    # Atualizando a lista de categorias
    combo_categoria_despesa['values'] = (categoria)

# Função inserir Receitas

def inserir_receita_b():
    nome = 'Receita'
    data = e_calreceitas.get()
    quantia = e_valor_receita.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i =='':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
        
    # chamando a função inserir receitas presente na view
    inserir_receita(lista_inserir)
    messagebox.showinfo('Sucesso','Dados inseridos com sucesso')

    e_calreceitas.delete(0,'end')
    e_valor_receita.delete(0,'end')

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# Função inserir Despesas

def inserir_despesas_b():
    nome = combo_categoria_despesa.get()
    data = e_cal_despesa.get()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i =='':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
        
    # chamando a função inserir despesas presente na view
    inserir_gasto(lista_inserir)
    messagebox.showinfo('Sucesso','Dados inseridos com sucesso')

    e_cal_despesa.delete(0,'end')
    e_valor_despesas.delete(0,'end')
    combo_categoria_despesa.delete(0,'end')

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# Função deletar categoria

def deletar_categoria_b():
    
    selecao = combo_categoria_despesa.get()

    if selecao == '':
        messagebox.showerror('Erro', 'Selecione no campo Categoria qual deve ser deletada')
    else:
        lista_cat = ver_categoria()
        new_list = []
        list_id = []

        for i in lista_cat:
            new_list.append(i[1])

        for i in lista_cat:
            list_id.append(i[0])
            
        pos= new_list.index(selecao)

        valor = list_id[pos]

        mensagem = messagebox.askyesno('Atenção','Deseja realmente deletar a categoria {}?'.format(selecao))
        
        if mensagem == True:
            deletar_categoria([valor])
            
            # Pegando os valores da categoria 
            categorias_funcao = ver_categoria()
            categoria = []

            for i in categorias_funcao:
                categoria.append(i[1])

            # Atualizando a lista de categorias
            combo_categoria_despesa['values'] = (categoria)
            combo_categoria_despesa.delete(0,'end')

            messagebox.showinfo('Sucesso','Categoria apagada com sucesso')
        else:
            messagebox.showinfo('Cancelado','Operação cancelada')
            combo_categoria_despesa.delete(0,'end')
    
# Função Deletar

def deletar_dados():
    try:
        mensagem = messagebox.askyesno('Atenção','Deseja realmente apagar esta informação?')
        if mensagem == True:
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            treev_lista = treev_dicionario['values']
            valor = treev_lista[0]
            nome = treev_lista[1]

            if nome == 'Receita':
                deletar_receitas([valor])
                messagebox.showinfo('Sucesso','Dados apagados com sucesso')
                # Atualizando dados
                mostrar_renda()
                porcentagem()
                grafico_bar()
                resumo()
                grafico_pie()
            else:
                deletar_gastos([valor])
                messagebox.showinfo('Sucesso','Dados apagados com sucesso')
                # Atualizando dados
                mostrar_renda()
                porcentagem()
                grafico_bar()
                resumo()
                grafico_pie()
        else:
            messagebox.showinfo('Cancelado','Operação cancelada')

    except IndexError:
        messagebox.showerror('Erro','Selecione um dos dados na tabela')

    '''
    except:
        messagebox.showwarning('Atenção','Para deletar apenas um item, selecione na tabela!')
        mensagem = messagebox.askyesno('Atenção','Deseja realmente apagar todos os dados da tabela?')
        
        if mensagem == True:
            deletar_tudo()
            
            # Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

            messagebox.showinfo('Sucesso','Categoria apagada com sucesso')
        else:
            messagebox.showinfo('Cancelado','Operação cancelada')
        '''

# Trabalhando no frameMeio

# Porcentagem

def porcentagem():
    l_nome = Label(frameMeio, text="Porcentagem da receita gasta", height=1, anchor=NW, font=("Verdana 12"), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar",background='#daed6b')
    style.configure("TProgressbar", thickness=25)
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')

    bar.place(x=10, y=35)
    bar['value'] = porcentagem_valor()

    valor = porcentagem_valor()

    if valor == None:
        valor = 0

    l_porcentagem = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=("Verdana 12"), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)

porcentagem()

# Função Grafico Barra

def grafico_bar():
    lista_categorias = ['Renda','Despesas','Saldo']
    lista_valores = bar_valores()

    # Faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    # ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores, color= colors, width=0.9)
    #create a list to collect the plt.patches data

    c = 0
    # set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias, fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

grafico_bar()

# Função de resumo total

def resumo():
    valor = bar_valores()

    # 1° linha
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)

    l_sumario = Label(frameMeio, text="Total Renda Mensal      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=35)

    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=70)

    # 2° linha
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=132)

    l_sumario = Label(frameMeio, text="Total Despesas Mensais   ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=115)

    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=150)

    # 3° linha
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=207)

    l_sumario = Label(frameMeio, text="Total saldo da caixa      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=190)

    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=220)

resumo()

# Função Grafico pie

def grafico_pie():
    # Faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5,3),dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    # Only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2),autopct='%1.1f%%',colors=colors, shadow=True, startangle=90)

    ax.legend(lista_categorias, loc='center right',bbox_to_anchor=(1.55 , 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0,column=0)

grafico_pie()

# Tabalhando frameBaixo

# Tabela Renda Mensal

app_tabela = Label(frameMeio, text="Tabela Receitas e Despesas", anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)

# Função para mostrar renda

def mostrar_renda():

    # creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

mostrar_renda()

# Configurações despesas

l_info = Label(frame_operacoes, text='Insira novas despesas',
                     height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

# Categoria

l_categoria = Label(frame_operacoes, text='Categoria',
                     height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

# Pegando categorias

categoria_funcao = ver_categoria()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesa = ttk.Combobox(frame_operacoes, width=12, font=('Ivy 10'))
combo_categoria_despesa['values'] = (categoria)
combo_categoria_despesa.place(x=110, y=41)

# Despesas

l_cal_despesas = Label(frame_operacoes, text='Data',
                     height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)

e_cal_despesa = DateEntry(frame_operacoes, width=12, background='darkblue', foreground='white', borderwidth=2,
                          year=2023)
e_cal_despesa.place(x=110, y=71)

# Valor 

l_valor_despesas = Label(frame_operacoes, text='Quantia Total',
                     height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)

e_valor_despesas = Entry(frame_operacoes, width=13, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)

# Botão Inserir nova despesa

img_add_despesas = Image.open('img/add.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)

botao_inserir_despesas = Button(frame_operacoes,command=inserir_despesas_b, image=img_add_despesas, text="Adicionar".upper()
                                , width=82, compound=LEFT,anchor=NW, font=('Ivy 7 bold')
                                , bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)

# Botão Excluir

l_excluir = Label(frame_operacoes, text='Excluir ação',
                     height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_excluir.place(x=10, y=190)

img_delete = Image.open('img/delete.png')
img_delete = img_delete.resize((17,17))
img_delete = ImageTk.PhotoImage(img_delete)

botao_deletar = Button(frame_operacoes,command=deletar_dados, image=img_delete, text="Deletar".upper()
                                , width=80, compound=LEFT,anchor=NW, font=('Ivy 7 bold')
                                , bg=co1, fg=co0, overrelief=RIDGE)
botao_deletar.place(x=110, y=183)

# Configurações Receitas

l_info = Label(frame_configuracao, text='Insira novas receitas',
                     height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

# Calendario 

l_cal_receitas = Label(frame_configuracao, text='Data',
                     height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)

e_calreceitas = DateEntry(frame_configuracao, width=12, background='darkblue', foreground='white', borderwidth=2,
                          year=2023)
e_calreceitas.place(x=110, y=41)

# Valor 

l_valor_receita = Label(frame_configuracao, text='Quantia Total',
                     height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receita.place(x=10, y=70)

e_valor_receita = Entry(frame_configuracao, width=13, justify='left', relief='solid')
e_valor_receita.place(x=110, y=71)

# Botão Inserir nova receita

img_add_receitas = Image.open('img/add.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)

botao_inserir_receitas = Button(frame_configuracao,command=inserir_receita_b, image=img_add_receitas, text="Adicionar".upper()
                                , width=82, compound=LEFT,anchor=NW, font=('Ivy 7 bold')
                                , bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=111)

# Operação nova Categoria

l_info = Label(frame_configuracao, text='Categoria',
                     height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=160)

e_categoria = Entry(frame_configuracao, width=13, justify='left', relief='solid')
e_categoria.place(x=110, y=160)

# Botão Inserir categoria

img_add_categoria = Image.open('img/add.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)

botao_inserir_categoria = Button(frame_configuracao,command=inserir_categoria_b, image=img_add_categoria, text="Adicionar".upper()
                                , width=82, compound=LEFT,anchor=NW, font=('Ivy 7 bold')
                                , bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_categoria.place(x=110, y=190)

# Botão remover categoria

img_delete_categoria = Image.open('img/delete.png')
img_delete_categoria = img_delete_categoria.resize((17,17))
img_delete_categoria = ImageTk.PhotoImage(img_delete_categoria)

botao_delete_categoria = Button(frame_configuracao,command=deletar_categoria_b, image=img_delete_categoria, text="Remover".upper()
                                , width=82, compound=LEFT,anchor=NW, font=('Ivy 7 bold')
                                , bg=co1, fg=co0, overrelief=RIDGE)
botao_delete_categoria.place(x=0, y=190)

janela.mainloop()