#Projeto do 4 bimestre de Banco de Dados
#Pedro R. / KAio S. / Bruno O.
#MongoBD
#CRIPTO=====> Derivação de chave com PBKDF2 + AES para armazenar feiti ̧cos.
#Hash como modo de criptografar
#Parte visual usando tkinter
#ABERTURA DE BANCO NO
import pymongo
import hashlib
from tkinter import *

# --- VARIÁVEIS GLOBAIS ---
idd = ""
senha = ""
nomemagia = ""
dificuldade = ""
x = ""
ing = ""

#BD e conexão
CONEXAO_STRING = "mongodb+srv://ProjetoMAN:666@projetobd4.mpst8h7.mongodb.net/?retryWrites=true&w=majority&appName=ProjetoBD4"

# --- FUNÇÕES DE LÓGICA ---

def gerar_hash(senha=""):
    hash_obj = hashlib.sha256(senha.encode())
    return hash_obj.hexdigest()

def conectar_bd():
    projeto = pymongo.MongoClient(CONEXAO_STRING)
    meu_banco = projeto['banco_de_dados']
    colecao = meu_banco['Grimório']
    return colecao

def inserir_grimorio():
    colecao = conectar_bd()
    global idd, senha, nomemagia, dificuldade, x
    
    # 1. Receber dados do entry
    idd = entrada_idade.get() 
    senha = entrada_senha.get()
    nomemagia = entrada_nomemagia.get()
    dificuldade = entrada_dificuldade.get()
    x = entrada_ingredientes.get()
    
    # Validação simples
    if not all([idd, senha, nomemagia, dificuldade, x]):
        # Se algum campo estiver vazio, não insere e informa ao usuário 
        print("Erro: Preencha todos os campos para a inserção.")
        return

    # 2. Criptografar senha com hash
    senha_cripto = gerar_hash(senha)
    
    # 3. Preparar o documento e inserir
    Magics = {
        "id": idd,
        "senha": senha_cripto,
        "nome_feitico": nomemagia,
        "dificuldade": dificuldade,
        "Ingredientes": x
    }
    try:
        colecao.insert_one(Magics)
        print(f"Grimório '{nomemagia}' inserido com sucesso!")
        
        # 4. Apagar para nova inserção
        entrada_idade.delete(0, END)
        entrada_senha.delete(0, END)
        entrada_nomemagia.delete(0, END)
        entrada_dificuldade.delete(0, END)
        entrada_ingredientes.delete(0, END)
        
    except Exception as e:
        print(f"Erro ao inserir no BD: {e}")

def selecionar_grimorio_bd():
    colecao = conectar_bd()
    global idd, senha
    
    # 1. Pegar apenas o ID e a Senha para busca
    idd = entrada_idade.get()
    senha = entrada_senha.get()
    
    if not all([idd, senha]):
        print("Erro: Digite o ID e a Senha para realizar a consulta.")
        return

    senha_cripto = gerar_hash(senha)
    
    # 2. Busca o documento pelo ID e compara a senha criptografada
    resultado = colecao.find_one({"id": idd})
    
    # 3. Limpa os campos após a tentativa de busca
    entrada_idade.delete(0, END)
    entrada_senha.delete(0, END)
    
    # 4. Processa o resultado
    if resultado:
        senha_recuperada = resultado.get("senha")
        
        
        if isinstance(senha_recuperada, dict):
             senha_recuperada = list(senha_recuperada.keys())[0] if senha_recuperada else None 
        
        if senha_recuperada == senha_cripto:
            # Dados do documento
            id_grim = resultado.get("id", "N/A")
            nome_grim = resultado.get("nome_feitico", "N/A")
            dificuldade_grim = resultado.get("dificuldade", "N/A")
            ing_grim = resultado.get("Ingredientes", "N/A")
            
            # Atualiza os labels finais de exibição
            numero.config(text=f"ID: {id_grim}")
            nome.config(text=f"Nome: {nome_grim}")
            dff.config(text=f"Dificuldade: {dificuldade_grim}")
            ingredientes.config(text=f"Ingredientes: {ing_grim}")
            print(f"Grimório de ID {id_grim} encontrado e exibido.")
        else:
            numero.config(text="Erro de Senha ou ID!", fg="yellow")
            nome.config(text="")
            dff.config(text="")
            ingredientes.config(text="")
            print("Senha ou ID incorretos.")
    else:
        numero.config(text="ID Não Encontrado!", fg="yellow")
        nome.config(text="")
        dff.config(text="")
        ingredientes.config(text="")
        print("Grimório com o ID fornecido não encontrado.")

# --- FUNÇÕES DE EXIBIÇÃO DA INTERFACE ---

def esconder_todos_campos():
    campos_e_labels = [
        label_idade, entrada_idade, label_senha, entrada_senha,
        label_nomemagia, entrada_nomemagia, label_dificuldade, entrada_dificuldade,
        label_ingredientes, entrada_ingredientes, botao_insercao, botao_selecao_acao
    ]
    for widget in campos_e_labels:
        widget.grid_forget()
    
    # Esconde os labels de resultado 
    labels_resultado = [numero, nome, dff, ingredientes]
    for widget in labels_resultado:
         widget.grid_forget()

def mostrar_insercao():
    esconder_todos_campos()
    
    # Exibe os labels e campos para Inserção
    label_idade.grid(column=0, row=5, padx=5, sticky='w')
    entrada_idade.grid(column=1, row=5, padx=5, pady=2, sticky='w')
    
    label_senha.grid(column=0, row=6, padx=5, sticky='w')
    entrada_senha.grid(column=1, row=6, padx=5, pady=2, sticky='w')
    
    label_nomemagia.grid(column=0, row=7, padx=5, sticky='w')
    entrada_nomemagia.grid(column=1, row=7, padx=5, pady=2, sticky='w')
    
    label_dificuldade.grid(column=0, row=8, padx=5, sticky='w')
    entrada_dificuldade.grid(column=1, row=8, padx=5, pady=2, sticky='w')
    
    label_ingredientes.grid(column=0, row=9, padx=5, sticky='w')
    entrada_ingredientes.grid(column=1, row=9, padx=5, pady=2, sticky='w')
    
    # Exibe o botão de Ação para Inserir
    botao_insercao.grid(column=1, row=10, pady=10)
    
    # Garante que o botão de Seleção de Ação esteja escondido 
    botao_selecao_acao.grid_forget()

def mostrar_selecao():
    esconder_todos_campos()
    
    # Exibe apenas os campos necessários para a Seleção (ID e Senha)
    label_idade.grid(column=0, row=5, padx=5, sticky='w')
    entrada_idade.grid(column=1, row=5, padx=5, pady=2, sticky='w')
    
    label_senha.grid(column=0, row=6, padx=5, sticky='w')
    entrada_senha.grid(column=1, row=6, padx=5, pady=2, sticky='w')
    
    # Exibe o botão de Ação para Selecionar 
    botao_selecao_acao.grid(column=1, row=7, pady=10)
    
    # Exibe os Labels onde o resultado será printado
    numero.grid(column=0, row=8, columnspan=2, sticky='w')
    nome.grid(column=0, row=9, columnspan=2, sticky='w')
    dff.grid(column=0, row=10, columnspan=2, sticky='w')
    ingredientes.grid(column=0, row=11, columnspan=2, sticky='w')

    # Esconde o botão de Inserção 
    botao_insercao.grid_forget()

#PARTE TKINTER
# --- JANELA PRINCIPAL ---
janela_principal = Tk()
janela_principal.title("Projeto Grimório-BD4")
janela_principal.config(bg='darkred')

# --- WIDGETS DE INTRODUÇÃO E ESCOLHA (Visíveis Sempre) ---
texto_intro = Label(janela_principal, text="Bem-vindo ao projeto 4 de BD!", background='darkred', fg="white")
texto_intro.grid(column=0, row=0, columnspan=2, pady=10)

texto1 = Label(janela_principal, text="Escolha dentre as opções:", background="darkred", fg="white")
texto1.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

escolha1 = Button(janela_principal, text="Inserir um novo grimório", command=mostrar_insercao, background="white", fg="black")
escolha2 = Button(janela_principal, text="Selecionar um grimório", command=mostrar_selecao, background="white", fg="black")

escolha1.grid(column=0, row=2, padx=10, pady=10)
escolha2.grid(column=1, row=2, padx=10, pady=10)

# --- WIDGETS DE ENTRADA  ---

# Labels auxiliares
label_idade = Label(janela_principal, text="ID:", background="darkred", fg="white")
label_senha = Label(janela_principal, text="Senha:", background="darkred", fg="white")
label_nomemagia = Label(janela_principal, text="Nome da Magia:", background="darkred", fg="white")
label_dificuldade = Label(janela_principal, text="Dificuldade:", background="darkred", fg="white")
label_ingredientes = Label(janela_principal, text="Ingredientes:", background="darkred", fg="white")

# Campos de entrada
entrada_idade = Entry(janela_principal, width=30, bd=3)
entrada_senha = Entry(janela_principal, width=30, bd=3, show="*") # * permite visualizar a senha, mantendo confidencial
entrada_nomemagia = Entry(janela_principal, width=30, bd=3)
entrada_dificuldade = Entry(janela_principal, width=30, bd=3)
entrada_ingredientes = Entry(janela_principal, width=30, bd=3)

# Botões de Ação Específicos
botao_insercao = Button(janela_principal, text="SALVAR GRIMÓRIO", command=inserir_grimorio, bg="green", fg="white")
botao_selecao_acao = Button(janela_principal, text="BUSCAR GRIMÓRIO", command=selecionar_grimorio_bd, bg="blue", fg="white")

# --- LABELS FINAIS DE RESULTADO  ---
numero = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)
nome = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)
dff = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)
ingredientes = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)

janela_principal.mainloop()