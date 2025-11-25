import os
import glob

base_path = r"[...]\xmls\cupons"

# Lista todas as pastas que começam com sat_store_
stores = glob.glob(os.path.join(base_path, "sat_store_*"))

for store_path in stores:
    print(f"Limpando pasta: {store_path}")

    # Lista todos os arquivos dentro da pasta
    for file_name in os.listdir(store_path):
        full_path = os.path.join(store_path, file_name)

        # Só remove arquivos
        if os.path.isfile(full_path):
            try:
                os.remove(full_path)
                print(f"  Apagado: {full_path}")
            except Exception as e:
                print(f"  Erro ao apagar {full_path}: {e}")

print("Processo finalizado.")
