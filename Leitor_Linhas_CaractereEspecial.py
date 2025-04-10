# Le as linhas do Parquet que contem caractere especial e retorna a linha anterior 
import pandas as pd
import re

# Lê o arquivo Parquet
df = pd.read_parquet(r"C:\Users\giuliano.gomes\Desktop\Ext_CRM_Pessoa\Ext_CRM_Pessoa.parquet")

# Garante que está ordenado da forma correta (se necessário, defina uma ordenação específica)
# df = df.sort_values(by='alguma_coluna_de_tempo_ou_ordem')

# Função para detectar caractere especial
def tem_caractere_especial(valor):
    return bool(re.search(r'[^a-zA-Z0-9_]', str(valor)))

# Cria uma coluna booleana para marcar as linhas com caractere especial
df['tem_especial'] = df['IDUNICO'].apply(tem_caractere_especial)

# Pega o IDUNICO da linha anterior onde tem_especial é True
idunico_linha_anterior = df.loc[df['tem_especial'], 'IDUNICO'].shift(1)

# Também podemos pegar os valores anteriores manualmente com o índice -1
linhas_com_anterior = df[df['tem_especial']].index - 1

# Filtra o DataFrame original com essas linhas anteriores (ignora -1 para não pegar índice inválido)
linhas_validas = df.loc[linhas_com_anterior[linhas_com_anterior >= 0]]

# Exibe os IDUNICO das linhas anteriores
print(linhas_validas['IDUNICO'])
