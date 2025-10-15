#Projeto 3 de POO- Pedro,Bruno, Kaio
#Projeto conectado com BD, database "univap"
#Projeto em python e MySQL que executa CRUD nas entidades: professores, disciplinas e professoresxdisciplinas
from prettytable import PrettyTable 
import mysql.connector
#abertura BD
contato=""
comandosql=""
#FUNÇÃO DE ABERTURA DO BANCO DE DADOS
#parametros de entrada, nenhum, output: return 0 e mensagem de funcionamento ou não
def AberturaBanco():
    try:
        global contato
        contato=mysql.connector.Connect(host='localhost',database='univap',user='root',password='')
        #mae240299 senha do alberson
        if contato.is_connected():
             #informacaobanco = contato.get_server_info()
            #  print(f"Banco de Dados: ABERTO; conexão realizada com sucesso")
             global comandosql 
             comandosql = contato.cursor()
             comandosql.execute('select database();')
             nomebanco = comandosql.fetchone()
            #  print(f'Banco de dados acessado = {nomebanco}') 
            #  print('='*70) 
             return 1 
        else: 
            print('Conexão não realizada com banco') 
            return 0 
    except Exception as erro: 
         print(f'Erro : {erro}') 
         return 0 
#Parte PROFESSORES
#Mostra os dados de todos os professores
def ShowProf():
    tabelao=PrettyTable()
    tabelao.field_names=['Registro do professor',"Nome","Telefone","Idade","Salario"]
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'SELECT * FROM professores;')
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0 :
            for linha in tabela :
                tabelao.add_row([f"{linha[0]}",f"{linha[1]}",f"{linha[2]}",f"{linha[3]}",f"{linha[4]}"])
                print(tabelao)
        else:
            print(f"Não há professores cadastrados")
    except Exception as erro:
        print(f' Ocorreu um  erro : {erro}')
#Mostra apenas os dados de um professor
def UmProf(registre=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f"select*from professores where registro={registre};")
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0 :
            for linha in tabela :
                print(f"Nome do professor(a): {linha[1]}")
                print(f"Telefone do professor(a): {linha[2]}")
                print(f"Idade do professor(a): {linha[3]}")
                print(f"Salário do professor(a):R$ {linha[4]}")
        #         return 'c'
        # else:
        #     return 'nc'
    except Exception as erro:
        print(f' Ocorreu um  erro na tentativa de consulta : {erro}')
#Cadastra um novo professor
def CadastraProf(registre=0,nprof="",telprof="",iprof=0,slprof=0):
    try:
         comandosql=contato.cursor()
         comandosql.execute(f'insert into professores (registro,nomeprof,telefoneprof,idadeprof,salarioprof) values ({registre},"{nprof}","{telprof}",{iprof},{slprof});')
         contato.commit()
         return 'Cadastro do professor(a) realizado com sucesso ! ' 
    except Exception as erro:
        print(f' Erro : {erro}')
        return 'Erro ao cadastrar professor(a) ! '
#Atualiza o cadastro de um professor
def AtualizaProf(registre=0,novoprof="",novotel="",novosl=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'update professores SET nomeprof="{novoprof}",telefoneprof="{novotel}",salarioprof={novosl} where registro={registre};')
        contato.commit()
        return 'Dados Atualizados com sucesso!'
    except Exception as erro:
         print(f"Erro:{erro}")
         return 'Não foi possível atualizar'
#Exclui um cadastro de professor
def ExcluiProf(registre=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'delete from professores where registro={registre};')
        contato.commit()
        return 'Cadastro excluido com sucesso'
    except Exception as erro:
         print(f"Erro:{erro}")
         print("Não é possível excluir um professor inexistente")
         print("Não é possível excluir professor que está cadastrado em disciplinasXprofessores")
         return 'Não foi possível excluir o cadastro'
#Parte DISCIPLINAS
#MOSTRA TODAS AS DISCIPLINAS
def ShowsGeral():
    tabelao=PrettyTable()
    tabelao.field_names=['Código das disciplinas',"Nomes das disciplinas"]
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'select*from disciplinas;')
        tabela=comandosql.fetchall()
        if comandosql.rowcount >0 :
            for linha in tabela :
                tabelao.add_row([f"{linha[0]}",f"{linha[1]}"])
            print (tabelao)
        else:
            print(f"Não há disciplinas cadastradas!")
    except Exception as erro:
        print(f"Ocorreu um erro:{erro}")
#SELECIONA APENAS UMA DISCIPLINA
def UmaDisciplina(cdisc=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f"select * from disciplinas where codigodisc={cdisc};")
        tabela=comandosql.fetchall()
        if comandosql.rowcount >0:
            for linha in tabela:
                print(f"Nome da disciplina: {linha[1]}")
        #         return 'c'
        # else:
        #     return 'nc'
    except Exception as erro:
        return (f"Ocorreu um erro na tentativa de consulta: Erro--->{erro}")
#CADASTRO DE DISCIPLINA
def CadastraDisc(cdisc=0,nd=""):
    try:
     comandosql=contato.cursor()
     comandosql.execute(f'insert into disciplinas (codigodisc,nomedisc) values ({cdisc},"{nd}");')
     contato.commit()
     return 'Cadastro da disciplina realizado com sucesso ! ' 
    except Exception as erro:
        print(f"Erro:{erro}")
        return 'Não foi possível cadastrar a disciplina!'
#ATUALIZAÇÃO DE DISCIPLINA
def AtualizarDisciplina(cdisc=0,nomenovo=""):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'update disciplinas SET nomedisc="{nomenovo}" where codigodisc={cdisc};')
        contato.commit()
        return 'Disciplina Atualizada com sucesso!'
    except Exception as erro:
        print(f"Erro:{erro}")
        return 'Não foi possível atualizar a disciplina'
#EXCLUSÃO DE DISCIPLINA
def TiraDisciplina(cdisc=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'delete from disciplinas where codigodisc={cdisc};')
        contato.commit()
        return 'Disciplina Excluída!'
    except Exception as erro:
        print(f"Erro:{erro}")
        print("Não é possível excluir uma disciplina inexistente")
        print("Não é possível excluir uma disciplina que está cadastrado em disciplinasXprofessores")
        return 'Não foi possível excluir'

#parte DISCIPLINASXPROFESSORES
#CADASTRA disciplinasxprofessores
def CadastraDiscXProf(CDNC=0,registre=0,codigodis=0,curss=0,CARH=0,Al=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'insert into disciplinasxprofessores (codigodisciplinanocurso,coddisciplina,codprofessor,curso,cargahoraria,anoletivo) values ({CDNC},{codigodis},{registre},{curss},{CARH},{Al});')
        contato.commit()
        return 'Cadastro realizado com sucesso!'
    except Exception as erro:
        print(f"Erro:{erro}")
        return 'Não foi possível cadastrar'
#TODOS OS DADOS  de disciplinasxprofessores
def DiscXProfsALL():
    tabelao=PrettyTable()
    tabelao.field_names=['Codigo DiscCurso',"Código Disc",'Codigo Prof',"Curso",'Carga Horária',"Ano Letivo"]
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'SELECT * FROM disciplinasxprofessores;')
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0:
            for linha in tabela:
                tabelao.add_row([f"{linha[0]}",f"{linha[1]}",f"{linha[2]}",f"{linha[3]}",f"{linha[4]}",f"{linha[5]}",f"{linha[6]}"])
                print(tabelao)
        else:
            print("Não há dados cadastrados!")
    except Exception as erro:
        print(f"Erro:{erro}")
#EXCLUI dados de disciplinaxprofessores
def ExcluiDiscXProf(CDNC=0):
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'delete from disciplinasxprofessores where codigodisciplinanocurso={CDNC};')
        contato.commit()
        return 'exclusão realizada com sucesso!'
    except Exception as erro:
         print(f"Erro{erro}")
         return 'Falha na exclusão'
#ATUALIZA dados de disciplinasxprofessores
def AtualizaDiscXProf():
    try:
        comandosql=contato.cursor()
        comandosql.execute(f'')
        contato.commit()
        return 'Atualização Feita com sucesso'
    except Exception as erro:
     print(f"Erro:{erro}")
     return 'Falha ao atualizar'
#MÓDULO PRINCIPAL (EL CABRÓN)
#Realização das funções para professores
x=AberturaBanco()
while x==1:
    try:
        resposta=int(input("\n Deseja entrar no modúlo de Professores? (1)\n Deseja entrar no módulo de diciplinas?  (2)\n Deseja entra na conexão disciplinas com professores?  (3)\n Qualquer outra tecla para sair!\n"))
        while resposta == 1 or resposta==2 or resposta==3:
            if resposta==1:
                print(f'='*70)
                print('{:^70}'.format('Sistema Univap-Profesores'))
                print(f'='*70)
                while True:
                    resp=int(input("Escolha uma opção: \n 0-visualizar todos os dados\n 1-escolher professor por id\n 2-cadastrar professor\n 3-excluir professor\n 4-atualizar professor\n"))
                    while  resp<0 and resp>4:
                        resp=int(input("Escolha DENTRE AS OPÇÕES:\n 0-visualizar todos os dados\n 1-escolher professor por id\n 2-cadastrar professor\n 3-excluir professor\n 4-atualizar professor\n"))
                    print("="*70)
                    if resp==0 :
                        x=AberturaBanco()
                        ShowProf()
                    if resp==1:
                        x=AberturaBanco()
                        registre=int(input("Insira o registro do professor para seleção de dados:\n"))
                        UmProf(registre)
                    if resp==2:
                        x=AberturaBanco()
                        registre=int(input("Insira o registro do professor:\n"))
                        nprof=input("Insira o nome do professor:\n")
                        print("insira o telefone no seguinte modelo: (DDD)99xxx-xxxx\n")
                        telprof=input("Insira o telefone do professor:\n")
                        while len(telprof) != 14:
                            telprof=input("Insira o telefone do professor corretamente:\n")

                        iprof=int(input("Insira a idade do professor:\n"))
                        slprof=float(input("Insira o salário do professor:\n"))
                        mensagem=CadastraProf(registre,nprof,telprof,iprof,slprof)
                        print(mensagem)
                    if resp==3:
                        x=AberturaBanco()
                        registre=int(input("Insira o registro do professor que será excluido:\n"))
                        confirmacao=input("ATENÇÃO! deseja de fato excluir? S-SIM ou N-NÃO\n")
                        while confirmacao!='S' and confirmacao!='N':
                            confirmacao=input("Resposta inexistente!!! - Deseja confirmar excusão S-SIM ou N-NÃO\n")
                        mensagem=ExcluiProf(registre)
                        print(mensagem)
                    if resp==4:
                            x=AberturaBanco()
                            print(f"ATENÇÃO! o código do Professor NÃO pode ser modificado")
                            registre=int(input("Insira o registro do professor que será atualizado:\n"))
                            novoprof =input("Insira o novo nome do professor:\n")
                            print("insira o telefone no seguinte modelo: (DDD)9xxx-xxxx\n")
                            novotel=input("Insira o novo telefone do professor:\n")
                            novosl=float(input("Insira o novo salário do professor:\n"))
                            mensagem=AtualizaProf(registre,novoprof,novotel,novosl)
                            print(mensagem)
                    if input("Deseja continuar usando o programa?? S-Sim OU qualquer tecla para finalizar:\n")=='S':
                        resposta=int(input("\n Deseja entrar no modúlo de Professores? (1)\n Deseja entrar no módulo de diciplinas?  (2)\n Deseja entra na conexão disciplinas com professores?  (3)\n Qualquer outra tecla para sair!\n"))
                        print("Fim do programa!!! obrigado pela preferência!")
                        print("="*70)
                        comandosql.close()
                        contato.close()
                        break
#Realização das funções para disciplinas
            if resposta==2:
                print(f'='*70)
                print('{:^70}'.format('Sistema Univap-Disciplinas'))
                print(f'='*70)
                while True:
                    resp=int(input("Escolha uma opção: \n 0-visualizar todos os dados\n 1-escolher disciplina por id\n 2-cadastrar disciplina\n 3-excluir disciplina\n 4-atualizar disciplina\n"))
                    while resp<0 and resp>4:
                        resp=int(input("Escolha DENTRE AS OPÇÕES:\n 0-visualizar todos os dados\n 1-escolher disciplina por id\n 2-cadastrar disciplina\n 3-excluir disciplina\n 4-atualizar disciplina\n"))
                    if resp==0:
                        x=AberturaBanco()
                        ShowsGeral()
                    if resp==1:
                        x=AberturaBanco()
                        codigodis=int(input("Insira o código da disciplina:\n"))
                        UmaDisciplina(codigodis)
                    if resp==2:
                        x=AberturaBanco()
                        codigodis=int(input("Insira o código da disciplina:\n"))
                        nomedisciplina=input("Insira o nome da disciplina:\n")
                        mensagem=CadastraDisc(codigodis,nomedisciplina)
                        print(mensagem)
                    if resp==3:
                        x=AberturaBanco()
                        codigodis=int(input("Insira o código da disciplina que deseja excluir:\n"))
                        confirmacao=input("ATENÇÃO! deseja de fato excluir? S-SIM ou N-NÃO\n")
                        while confirmacao!='S' and confirmacao!='N':
                         confirmacao=input("Resposta inexistente!!! - Deseja confirmar excusão S-SIM ou N-NÃO\n")
                        mensagem=TiraDisciplina(codigodis)
                        print(mensagem)
                    if resp==4:
                        x=AberturaBanco()
                        print(f"ATENÇÃO! o código da disciplina NÃO pode ser modificado")
                        codigodis=int(input("Insira o código da disciplina a ser atualizada:\n"))
                        nomedisciplina=input("Insira o novo nome da disciplina:")
                        mensagem=AtualizarDisciplina(codigodis,nomedisciplina)
                        print(mensagem)
                    print('\n\n')
                    print('='*70)
                    if input("Deseja continuar usando o programa?? S-Sim OU qualquer tecla para finalizar:")=='S':
                            resposta=int(input("\n Deseja entrar no modúlo de Professores? (1)\n Deseja entrar no módulo de diciplinas?  (2)\n Deseja entra na conexão disciplinas com professores?  (3)\n Qualquer outra tecla para sair!\n"))
                            print("Fim do programa!!! obrigado pela preferência!")
                            print("="*70)
                            comandosql.close()
                            contato.close()
                            break
#Parte disciplinasXprofessores
            if resposta==3:
                print(f'='*70)
                print('{:^70}'.format('Sistema Univap-DisciplinasxProfessores'))
                print(f'='*70)
                while True:
                    resp=int(input("Escolha uma opção: \n 0-visualizar todos os dados\n 1-escolher Disciplina do curso por id\n 2-cadastrar dados\n 3-excluir dados\n 4-atualizar dados\n"))
                    while  resp<0 and resp>4:
                        resp=int(input("Escolha DENTRE AS OPÇÕES:\n 0-visualizar todos os dados\n 1-escolher dado por id\n 2-cadastrar dados\n 3-excluir dados\n 4-atualizar dados\n"))
                    print("="*70)
                    if resp==0:
                        x=AberturaBanco()
                        DiscXProfsALL()
                    if resp==2:
                        x=AberturaBanco()
                        CDNC=int(input("Insira o código da disciplina do curso:\n"))
                        codigodis=int(input("Insira o código da disciplina:\n"))
                        registre=int(input("Insira o registro do professor(a):\n"))
                        curss=int(input("Insira o curso:\n"))
                        CARH=int(input("Insira a carga horária em horas:\n"))
                        Al=int(input("Insira o ano letivo:\n"))
                        mensagem=CadastraDiscXProf(CDNC,registre,codigodis,curss,CARH,Al)
                        print(mensagem)
                    if resp==3:
                        x=AberturaBanco()
                        CDNC=int(input("Insira o código do dado para exclusão\n"))
                        confirmacao=input("ATENÇÃO! deseja de fato excluir? S-SIM ou N-NÃO\n")
                        while confirmacao!='S' and confirmacao!='N':
                          confirmacao=input("Resposta inexistente!!! - Deseja confirmar excusão S-SIM ou N-NÃO\n")
                        mensagem=ExcluiDiscXProf(CDNC)
                        print(mensagem)
                    if resp==4:
                        x=AberturaBanco()
                        print(f"ATENÇÃO! o código da disciplina no curso NÃO pode ser modificado")
                        CDNC=int(input("Insira o código dos dados à atualizar\n"))
                        codigodis=int(input("Insira o  novo código da disciplina:\n"))
                        registre=int(input("Insira o  registro novo:\n"))
                        curss=int(input("Insira o novo curso:\n"))
                        CARH=int(input("Insira a  nova carga horária em horas:\n"))
                        Al=int(input("Insira o  novo ano letivo:\n"))
                        mensagem=AtualizaDiscXProf(CDNC,codigodis,registre,curss,CARH,Al)
                        print(mensagem)
                    print('\n\n')
                    print('='*70)
                    if input("Deseja continuar usando o programa?? S-Sim OU qualquer tecla para finalizar:")=='S':
                        resposta=int(input("\n Deseja entrar no modúlo de Professores? (1)\n Deseja entrar no módulo de diciplinas?  (2)\n Deseja entra na conexão disciplinas com professores?  (3)\n Qualquer outra tecla para sair!\n"))
                        print("Fim do programa!!! obrigado pela preferência!")
                        print("="*70)
                        comandosql.close()
                        contato.close()
                        break
    except Exception as erro:
     print(f"Erro{erro}")