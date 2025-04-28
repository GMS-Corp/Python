import os

# Diretório base onde estão os diretórios das lojas
base_dir = r"V:"

# Loop para cada loja de 001 até 058
for i in range(1, 59):
    loja = os.path.join(f'loja{i:02d}', 'pdv', 'arquivos')
    full_path = os.path.join(base_dir, loja)
    
    if os.path.exists(full_path) and os.path.isdir(full_path):
        # Conta apenas arquivos (não subpastas)
        num_arquivos = len([f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))])
    else:
        num_arquivos = 0  # Se não existir o diretório, considera 0 arquivos
    
    # Adiciona à lista
    print(f'{loja}: {num_arquivos} arquivos')
