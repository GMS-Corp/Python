# Converte CSV para PARQUET 

import os
import pandas as pd

# Diretório onde estão os arquivos CSV
diretorio = r"C:\Users\giuliano.gomes\Desktop\Ext_CRM_Pessoa_v2"

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

            # Verifica se a coluna DATVENDA existe
            if 'DATVENDA' in df.columns:
                # Converte para datetime e mantém o formato UTC
                df['DATVENDA'] = pd.to_datetime(df['DATVENDA'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
                df['DATVENDA'] = df['DATVENDA'].dt.tz_localize('America/Sao_Paulo')  # Define como UTC

            # Define o nome do arquivo Parquet
            nome_parquet = arquivo.replace(".csv", ".parquet")
            caminho_parquet = os.path.join(diretorio, nome_parquet)

            # Salva no formato Parquet
            df.to_parquet(caminho_parquet, engine="pyarrow", compression="snappy")

            print(f"Convertido: {nome_parquet}")

        except Exception as e:
            print(f"Erro ao converter {arquivo}: {e}")

print("Conversão concluída")
