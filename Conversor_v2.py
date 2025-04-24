# Converte CSV para PARQUET 

import os
import pandas as pd

# Diretório onde estão os arquivos CSV
diretorio = r"C:\Users\giuliano.gomes\Desktop\pasta"

# Loop para percorrer todos os arquivos no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.startswith("Ext_") and arquivo.endswith(".csv"):  # Filtra apenas os arquivos desejados
        caminho_csv = os.path.join(diretorio, arquivo) 

        print(f"Convertendo: {arquivo}...")
        

        try:
            # Lê o CSV
            df = pd.read_csv(
                caminho_csv, 
                delimiter=";", 
                encoding="latin1",  # Alterado para maior compatibilidade
                engine="python",  # Usa o motor Python para evitar buffer overflow
                on_bad_lines="skip"  # Ignora linhas problemáticas
            )
            print(df[['DTAPRIMCOMPRA', 'DTAULTCOMPRA']].head(10)) #So pra checar o formato antes

            # Verifica se a coluna DATVENDA existe
            if 'DTAPRIMCOMPRA' in df.columns:
                # Converte para datetime e mantém o formato UTC
                df['DTAPRIMCOMPRA'] = pd.to_datetime(df['DTAPRIMCOMPRA'], format='%d-%b-%y', errors='coerce')
            if 'DTAULTCOMPRA' in df.columns:
                # Converte para datetime e mantém o formato UTC
                df['DTAULTCOMPRA'] = pd.to_datetime(df['DTAULTCOMPRA'], format='%d-%b-%y', errors='coerce')

            # Define o nome do arquivo Parquet
            nome_parquet = arquivo.replace(".csv", ".parquet")
            caminho_parquet = os.path.join(diretorio, nome_parquet)

            # Salva no formato Parquet
            df.to_parquet(caminho_parquet, engine="pyarrow", compression="snappy")

            print(f"Convertido: {nome_parquet}")

        except Exception as e:
            print(f"Erro ao converter {arquivo}: {e}")

print("Conversão concluída")
