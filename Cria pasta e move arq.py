import os
import glob
import shutil

base_path = r"\\[[diretorio]]\cupons"

sat_folders = glob.glob(os.path.join(base_path, "sat_store_*"))

for sat_path in sat_folders:
    folder_name = os.path.basename(sat_path)
    num = folder_name.replace("sat_store_", "")

    ent_folder = os.path.join(base_path, f"ent_store_{num}")
    saida_folder = os.path.join(base_path, f"saidas_store_{num}")

    # Criar pastas
    os.makedirs(ent_folder, exist_ok=True)
    os.makedirs(saida_folder, exist_ok=True)

    print(f"\nProcessando loja {num}")

    # =============================
    # LIMPAR DESTINOS
    # =============================
    for folder in [ent_folder, saida_folder]:
        for item in os.listdir(folder):
            path = os.path.join(folder, item)

            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)      # remove arquivo
                elif os.path.isdir(path):
                    shutil.rmtree(path) # remove subpasta
            except Exception as e:
                print(f"Erro ao remover {path}: {e}")

    print(f"\nProcessando loja {num}")

    # =============================
    # 1. MOVER DO SAT
    # =============================
    for file_name in os.listdir(sat_path):
        src = os.path.join(sat_path, file_name)

        if not os.path.isfile(src):
            continue

        try:
            # REGRA: define destino
            if "SAIDA" in file_name.upper():
                dst = os.path.join(saida_folder, file_name)
            else:
                dst = os.path.join(ent_folder, file_name)

            shutil.move(src, dst)
            print(f"Movido do SAT: {file_name}")

        except Exception as e:
            print(f"Erro ao mover {file_name}: {e}")

    # =============================
    # 2. CORRIGIR O QUE JÁ FOI ERRADO (ENT → SAIDAS)
    # =============================
    for file_name in os.listdir(ent_folder):
        src = os.path.join(ent_folder, file_name)

        if not os.path.isfile(src):
            continue

        if "SAIDA" in file_name.upper():
            try:
                dst = os.path.join(saida_folder, file_name)
                shutil.move(src, dst)
                print(f"Corrigido (ENT → SAIDA): {file_name}")
            except Exception as e:
                print(f"Erro ao corrigir {file_name}: {e}")

print("\nProcesso concluído.")
