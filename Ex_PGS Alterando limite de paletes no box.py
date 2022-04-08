#IMPORTAR PSYCOPG2 CONFIG
import datetime
import psycopg2

#PARAMETOS CONEXAO
host = 'localhost'
dbname = 'CD_EXP'
user = 'postgres'
password = 'nag1234'

#FORMATO CONEXAO
conn_string = 'host={0} user={1} dbname={2} password={3}'.format(host, user, dbname, password)

#TESTES CHAMADA FUNCAO NO BANCO - IMPUT
Loja = input("Digite o Número da Loja: ")
PL = input("Digite a quantidade MAXIMA de paletes: ")
print("Dados Informados: Loja:", Loja, "Maximo de Paletes:", PL)

#CONFIRMACAO UPDATE
PAD = input("Confirmar alteração?: ")
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")
#conn = psycopg2.connect(conn_string)
#pPPL = conn.cursor()
#pPPL.execute(f"SELECT MAX(PL_OCUPADOS) FROM CD_BOXES WHERE loja = {Loja}")
#pPlresult = pPPL.fetchone()

#CHECK RESULTADOS
if PAD.lower() == "sim":
    conn = psycopg2.connect(conn_string)
    conex = conn.cursor()
    conex.execute(f"""CALL pcd_plup({Loja},{PL})""")
    conn.commit()
    print("\nQuantidade maxima de paletes alterado na Loja",Loja,
          "\n""(",PL,"Paletes MAX )"
          "\n""Data:", dt_string)
else:
    print("Alteração Cancelada!")
