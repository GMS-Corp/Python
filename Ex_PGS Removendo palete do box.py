import psycopg2

host     = 'localhost'
dbname   = 'CD_EXP'
user     = 'postgres'
password = 'nag1234'

conn_string = 'host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)

Loja = input("Digite o Número da Loja: ")

conn = psycopg2.connect(conn_string)
conex = conn.cursor()
conex.execute(f"""SELECT CASE WHEN PL_Ocupados BETWEEN 1 AND ((SELECT MAX(PL_MAX) FROM cd_boxes)-1) 
                                       THEN 'Parcialmente Ocupado' 
                 WHEN PL_Ocupados = 13 THEN 'Box Cheio'
                 WHEN PL_Ocupados = 0  THEN 'Box Livre' END
                 FROM cd_boxes where Loja = {Loja};""")
myresult = conex.fetchone()

if myresult == ('Box Cheio',):
    conexao = conn.cursor()
    conexao.execute(f"""CALL pcd_repl({Loja})""")
    conn.commit()
    print("Pl Retirado")
elif myresult == ('Parcialmente Ocupado,'):
    conexao = conn.cursor()
    conexao.execute(f"""CALL p=cd_repl({Loja})""")
    conn.commit()
    print("PL Retirado")
else:
    print("Atenção! Box Vazio. Não há paletes à serem retirados!")