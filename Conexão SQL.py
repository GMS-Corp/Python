#EXEMPLO CONEXAO POSTGRESQL

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
