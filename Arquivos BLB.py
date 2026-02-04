
import os
import glob
import shutil

base_path = r"\\10.110.160.15\consinco-arquivos\xmls\cupons"

# Lista todas as pastas sat_store_xxx
sat_folders = glob.glob(os.path.join(base_path, "sat_store_*"))

def limpar_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        return

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            os.remove(caminho)

for sat_path in sat_folders:
    folder_name = os.path.basename(sat_path)           # sat_store_002
    num = folder_name.replace("sat_store_", "")        # 002

    ent_folder = os.path.join(base_path, f"ent_store_{num}")
    saidas_folder = os.path.join(base_path, f"saidas_store_{num}")

    # Criar e limpar pastas de destino
    limpar_pasta(ent_folder)
    limpar_pasta(saidas_folder)

    print(f"Processando {sat_path}")

    # Processar arquivos da pasta sat_store_xxx
    for file_name in os.listdir(sat_path):
        src = os.path.join(sat_path, file_name)

        if not os.path.isfile(src):
            continue

        file_upper = file_name.upper()

        try:
            if "ENTRADAS" in file_upper:
                dst = os.path.join(ent_folder, file_name)
                shutil.move(src, dst)
                print(f"  ENTRADA -> {file_name}")

            elif "SAIDAS" in file_upper:
                dst = os.path.join(saidas_folder, file_name)
                shutil.move(src, dst)
                print(f"  SAIDA   -> {file_name}")

            else:
                print(f"  Ignorado (nome nao reconhecido): {file_name}")

        except Exception as e:
            print(f"  Erro ao mover {file_name}: {e}")

print("Processo concluido.")
