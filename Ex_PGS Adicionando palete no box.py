#IMPORTAR PSYCOPG2 CONFIG PARA CONECTAR  SQL
import datetime
import psycopg2

#PARAMETOS CONEXAO
host      = 'localhost'
dbname    = 'CD_EXP'
user      = 'postgres'
password  = 'nag1234'

#FORMATO CONEXAO
conn_string = 'host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)

Loja = input("Digite o Número da Loja: ")

conn = psycopg2.connect(conn_string) #PRECISA CRIAR CONECTOR E CURSOR
conex = conn.cursor()

#EXECUTA CURSOR * Cursos que pesquisa e seta o status do box (exemplo)
conex.execute(f"""SELECT CASE WHEN PL_Ocupados BETWEEN 1 AND ((SELECT MAX(PL_MAX) FROM cd_boxes)-1) 
                                       THEN 'Parcialmente Ocupado' 
                 WHEN PL_Ocupados = 13 THEN 'Box Cheio'
                 WHEN PL_Ocupados = 0  THEN 'Box Livre' END
                 FROM cd_boxes where Loja = {Loja};""")
myresult = conex.fetchone()

if myresult == ('Box Livre',):
    conexao = conn.cursor()
    conexao.execute(f"""CALL pcd_adpl({Loja})""")
    conn.commit()
    print("Pl Adicionado")
elif myresult == ('Parcialmente Ocupado,'):
    conexao = conn.cursor()
    conexao.execute(f"""CALL pcd_adpl({Loja})""")
    conn.commit()
    print("PL Adicionado")
else:
    print("Atenção! Box Cheio. Palete NÃO Adicionado!")