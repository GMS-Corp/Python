import os
import glob
import shutil

base_path = r"[...]\xmls\cupons"

# Lista todas as pastas sat_store_xxx
sat_folders = glob.glob(os.path.join(base_path, "sat_store_*"))

for sat_path in sat_folders:
    folder_name = os.path.basename(sat_path)           # exemplo: sat_store_002
    num = folder_name.replace("sat_store_", "")        # exemplo: 002

    ent_folder = os.path.join(base_path, f"ent_store_{num}")

    # Criar pasta ent_store_xxx se não existir
    os.makedirs(ent_folder, exist_ok=True)

    print(f"Movendo arquivos de {sat_path} para {ent_folder}")

    # Listar arquivos da pasta sat_store_xxx
    for file_name in os.listdir(sat_path):
        src = os.path.join(sat_path, file_name)
        dst = os.path.join(ent_folder, file_name)

        if os.path.isfile(src):
            try:
                shutil.move(src, dst)
                print(f"  Movido: {file_name}")
            except Exception as e:
                print(f"  Erro ao mover {file_name}: {e}")

print("Processo concluído.")
