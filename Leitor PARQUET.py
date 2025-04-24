import os
import pandas as pd

# Lê o arquivo Parquet
df = pd.read_parquet(r"C:\Users\giuliano.gomes\Desktop\pasta\Ext_CRM_Pessoa_Full.parquet")
print(df.dtypes)
# Filtra onde IDPESSOA é igual a um valor específico, por exemplo 12345
id_desejado = "51410065812"
resultado = df.loc[df["IDPESSOA"] == id_desejado, ["IDUNICO", "TXTNOMECOMPLETO", "DTAPRIMCOMPRA", "DTAULTCOMPRA"]]

# Exibe a linha filtrada
print(resultado)
