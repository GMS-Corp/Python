# Le e checka os valores/colunas do PARQUET

import os
import pandas as pd

df = pd.read_parquet(r"\\10.110.160.15\consinco-arquivos\plusoft\2_Ext_v3_Vda_ABR_2023.parquet")
print(df.dtypes)
print(df.head())
