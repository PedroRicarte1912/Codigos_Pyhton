#Projeto do 4 bimestre de Banco de Dados
#Pedro R. / KAio S. / Bruno O.
#MongoBD
#CRIPTO=====> Derivacao de chave com PBKDF2 + AES para armazenar feiticos.
#Hash como modo de criptografar
#Parte visual usando tkinter
#ABERTURA DE BANCO NO
import pymongo
import os # Para gerar o Salt
from tkinter import *
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.backends import default_backend

# --- VARIAVEIS GLOBAIS ---
idd = ""
senha = ""
nomemagia = ""
dificuldade = ""
x = ""
ing = ""

# --- CONFIGURACOES CRIPTOGRAFICAS ---
ITERATIONS = 600000 
KEY_LENGTH = 32     # 256 bits para AES-256

#BD e conexao
CONEXAO_STRING = "mongodb+srv://ProjetoMAN:666@projetobd4.mpst8h7.mongodb.net/?retryWrites=true&w=majority&appName=ProjetoBD4"

# --- FUNCOES DE LOGICA CRIPTOGRAFICA ---

def gerar_chave_pbkdf2(senha_bytes: bytes, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(senha_bytes)

def criptografar_dado(chave: bytes, dado_simples: str):
    aesgcm = AESGCM(chave)
    
    nonce = os.urandom(12) 
    dado_bytes = dado_simples.encode('utf-8')
    
    texto_cifrado_e_tag = aesgcm.encrypt(nonce, dado_bytes, None)
    
    return nonce, texto_cifrado_e_tag

def descriptografar_dado(chave: bytes, nonce: bytes, texto_cifrado_e_tag: bytes):
    """Descriptografa um dado com AES-256 GCM e verifica a Tag de AutenticaCao."""
    aesgcm = AESGCM(chave)
    try:
        dado_descriptografado = aesgcm.decrypt(nonce, texto_cifrado_e_tag, None)
        return dado_descriptografado.decode('utf-8')
    except Exception as e:
        # Se a descriptografia falhar (erro na chave ou nos dados), retorna None
        print(f"Erro ao descriptografar: {e}")
        return None

# --- FUNCOES DE LOGICA DE BANCO DE DADOS ---

def conectar_bd():
    projeto = pymongo.MongoClient(CONEXAO_STRING)
    meu_banco = projeto['banco_de_dados']
    colecao = meu_banco['GrimOrio']
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
    
    # ValidaCao simples
    if not all([idd, senha, nomemagia, dificuldade, x]):
        print("Erro: Preencha todos os campos para a inserCao.")
        return

    # --- CRIPTOGRAFIA PARA INSERCaO ---
    # Gerar Salt e Chave
    salt = os.urandom(16) # 16 bytes de Salt
    chave = gerar_chave_pbkdf2(senha.encode(), salt)
    
    # Criptografar cada campo
    nonce_nome, cifrado_nome = criptografar_dado(chave, nomemagia)
    nonce_dificuldade, cifrado_dificuldade = criptografar_dado(chave, dificuldade)
    nonce_ing, cifrado_ing = criptografar_dado(chave, x)
    
    # 3. Preparar o documento com todos os parâmetros criptogrAficos e inserir
    Magics = {
        "id": idd,
        "salt": salt, # O salt eh armazenado em texto plano
        "nome_feitico_cifrado": cifrado_nome,
        "nonce_nome": nonce_nome,
        "dificuldade_cifrada": cifrado_dificuldade,
        "nonce_dificuldade": nonce_dificuldade,
        "ingredientes_cifrado": cifrado_ing,
        "nonce_ingredientes": nonce_ing,
        "iteracoes_pbkdf2": ITERATIONS 
    }
    
    try:
        colecao.insert_one(Magics)
        print(f"Grimório '{nomemagia}' inserido e CRIPTOGRAFADO com sucesso!")
        
        # 4. Apagar para nova inserCao
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

    # 2. Busca o documento pelo ID
    resultado = colecao.find_one({"id": idd})
    
    # 3. Limpa os campos após a tentativa de busca
    entrada_idade.delete(0, END)
    entrada_senha.delete(0, END)
    
    # 4. Processa o resultado
    if resultado:
        # --- DESCRIPTOGRAFIA ---
        salt = resultado.get("salt")
        
        if not salt:
            print("Erro: GrimOrio encontrado, mas faltando parâmetros de seguranCa (Salt).")
            return

        # 4.1. Gerar a mesma chave
        chave = gerar_chave_pbkdf2(senha.encode(), salt)
        
        # 4.2. Tentar descriptografar o Nome do FeitiCo como teste de senha
        cifrado_nome = resultado.get("nome_feitico_cifrado")
        nonce_nome = resultado.get("nonce_nome")
        
        nome_descriptografado = descriptografar_dado(chave, nonce_nome, cifrado_nome)
        
        if nome_descriptografado is not None:
            # Senha Correta! Descriptografa os outros dados.
            cifrado_dificuldade = resultado.get("dificuldade_cifrada")
            nonce_dificuldade = resultado.get("nonce_dificuldade")
            
            cifrado_ing = resultado.get("ingredientes_cifrado")
            nonce_ing = resultado.get("nonce_ingredientes")

            dificuldade_descriptografada = descriptografar_dado(chave, nonce_dificuldade, cifrado_dificuldade)
            ing_descriptografado = descriptografar_dado(chave, nonce_ing, cifrado_ing)
            
            # 4.3. Atualiza os labels finais de exibiCao
            numero.config(text=f"ID: {idd}")
            nome.config(text=f"Nome: {nome_descriptografado}")
            dff.config(text=f"Dificuldade: {dificuldade_descriptografada}")
            ingredientes.config(text=f"Ingredientes: {ing_descriptografado}")
            print(f"GrimOrio de ID {idd} encontrado e descriptografado com sucesso.")
        else:
            # Senha Incorreta
            numero.config(text="Erro de Senha ou ID!", fg="yellow")
            nome.config(text="")
            dff.config(text="")
            ingredientes.config(text="")
            print("Senha incorreta ou erro de integridade nos dados (Tag GCM falhou).")
    else:
        # ID Nao Encontrado
        numero.config(text="ID Nao Encontrado!", fg="yellow")
        nome.config(text="")
        dff.config(text="")
        ingredientes.config(text="")
        print("GrimOrio com o ID fornecido nao encontrado.")

# --- FUNCÕES DE EXIBICaO DA INTERFACE ---

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
    
    # Exibe os labels e campos para InserCao
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
    
    # Exibe o botao de ACao para Inserir
    botao_insercao.grid(column=1, row=10, pady=10)
    
    # Garante que o botao de SeleCao de ACao esteja escondido 
    botao_selecao_acao.grid_forget()

def mostrar_selecao():
    esconder_todos_campos()
    
    # Exibe apenas os campos necessArios para a SeleCao (ID e Senha)
    label_idade.grid(column=0, row=5, padx=5, sticky='w')
    entrada_idade.grid(column=1, row=5, padx=5, pady=2, sticky='w')
    
    label_senha.grid(column=0, row=6, padx=5, sticky='w')
    entrada_senha.grid(column=1, row=6, padx=5, pady=2, sticky='w')
    
    # Exibe o botao de ACao para Selecionar 
    botao_selecao_acao.grid(column=1, row=7, pady=10)
    
    # Exibe os Labels onde o resultado serA printado
    numero.grid(column=0, row=8, columnspan=2, sticky='w')
    nome.grid(column=0, row=9, columnspan=2, sticky='w')
    dff.grid(column=0, row=10, columnspan=2, sticky='w')
    ingredientes.grid(column=0, row=11, columnspan=2, sticky='w')

    # Esconde o botao de InserCao 
    botao_insercao.grid_forget()

#PARTE TKINTER
# --- JANELA PRINCIPAL ---
janela_principal = Tk()
janela_principal.title("Projeto GrimOrio-BD4 (PBKDF2 + AES)")
janela_principal.config(bg='darkred')

# --- WIDGETS DE INTRODUCaO E ESCOLHA (Visíveis Sempre) ---
texto_intro = Label(janela_principal, text="Bem-vindo ao projeto 4 de BD!", background='darkred', fg="white")
texto_intro.grid(column=0, row=0, columnspan=2, pady=10)

texto1 = Label(janela_principal, text="Escolha dentre as opCões:", background="darkred", fg="white")
texto1.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

escolha1 = Button(janela_principal, text="Inserir um novo grimOrio", command=mostrar_insercao, background="white", fg="black")
escolha2 = Button(janela_principal, text="Selecionar um grimOrio", command=mostrar_selecao, background="white", fg="black")

escolha1.grid(column=0, row=2, padx=10, pady=10)
escolha2.grid(column=1, row=2, padx=10, pady=10)

# --- WIDGETS DE ENTRADA  ---

# Labels auxiliares
label_idade = Label(janela_principal, text="ID:", background="darkred", fg="white")
label_senha = Label(janela_principal, text="Senha Mestra:", background="darkred", fg="white")
label_nomemagia = Label(janela_principal, text="Nome da Magia:", background="darkred", fg="white")
label_dificuldade = Label(janela_principal, text="Dificuldade:", background="darkred", fg="white")
label_ingredientes = Label(janela_principal, text="Ingredientes:", background="darkred", fg="white")

# Campos de entrada
entrada_idade = Entry(janela_principal, width=30, bd=3)
entrada_senha = Entry(janela_principal, width=30, bd=3, show="*") 
entrada_nomemagia = Entry(janela_principal, width=30, bd=3)
entrada_dificuldade = Entry(janela_principal, width=30, bd=3)
entrada_ingredientes = Entry(janela_principal, width=30, bd=3)

# Botões de ACao Específicos
botao_insercao = Button(janela_principal, text="SALVAR GRIMORIO", command=inserir_grimorio, bg="green", fg="white")
botao_selecao_acao = Button(janela_principal, text="BUSCAR GRIMORIO", command=selecionar_grimorio_bd, bg="blue", fg="white")

# --- LABELS FINAIS DE RESULTADO  ---
numero = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)
nome = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)
dff = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)
ingredientes = Label(janela_principal, text="", background="darkred", fg="white", justify=LEFT)

janela_principal.mainloop()