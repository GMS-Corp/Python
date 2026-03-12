#Le emails e grava o XML no clob do oracle

import win32com.client
import os
import datetime
import oracledb

print("=== INICIANDO PROCESSAMENTO ===")

# -------------------------------
# CONEXÃO ORACLE
# -------------------------------

oracledb.init_oracle_client(
    lib_dir=r"C:\app\client\oracle12c\product\12.2.0\client_1\bin"
)

conn = oracledb.connect(
    user="usuario",
    password="senha",
    dsn="dns"
)

cursor = conn.cursor()
print("Conectado ao Oracle")

# -------------------------------
# CONEXÃO OUTLOOK
# -------------------------------

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
root = outlook.Folders["com.br"]
inbox = root.Folders["Caixa de Entrada"]
processados = root.Folders["Processados"]

if processados is None:
    raise Exception("Pasta 'Processados' não encontrada")

print("Conectado ao Outlook")

# -------------------------------
# PASTA TEMP
# -------------------------------

temp_path = r"C:\temp\xml_email"
os.makedirs(temp_path, exist_ok=True)
print("Pasta temporária:", temp_path)

# -------------------------------
# CONTADORES
# -------------------------------

total_emails = 0
xml_processados = 0

# -------------------------------
# PEGAR EMAILS DE HOJE NÃO LIDOS
# -------------------------------

messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

hoje = datetime.date.today()
emails_hoje_nao_lidos = []

for msg in list(messages):
    if msg.Class != 43:  # só processa emails
        continue
    data_email = msg.ReceivedTime.replace(tzinfo=None).date()
    if data_email == hoje and msg.UnRead:
        emails_hoje_nao_lidos.append(msg)

print(f"Emails não lidos de hoje: {len(emails_hoje_nao_lidos)}")

# -------------------------------
# PROCESSAMENTO
# -------------------------------

for msg in emails_hoje_nao_lidos:
    try:
        total_emails += 1
        print("Email:", msg.Subject)

        encontrou_xml = False

        if msg.Attachments.Count > 0:
            for att in msg.Attachments:
                if att.FileName.lower().endswith(".xml"):
                    encontrou_xml = True
                    caminho = os.path.join(temp_path, att.FileName)

                    # Evita sobrescrever arquivo com mesmo nome
                    if os.path.exists(caminho):
                        base, ext = os.path.splitext(att.FileName)
                        contador = 1
                        while os.path.exists(os.path.join(temp_path, f"{base}_{contador}{ext}")):
                            contador += 1
                        caminho = os.path.join(temp_path, f"{base}_{contador}{ext}")

                    att.SaveAsFile(caminho)
                    print("XML salvo:", caminho)

                    # lê o conteúdo do XML
                    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                        xml = f.read()

                    # insere no Oracle
                    cursor.execute("""
                        INSERT INTO EMAIL_XML_IMPORT
                        (
                            DATA_EMAIL,
                            REMETENTE,
                            ASSUNTO,
                            NOME_ARQUIVO,
                            XML_CONTEUDO
                        )
                        VALUES
                        (:1,:2,:3,:4,:5)
                    """,
                    (
                        msg.ReceivedTime,
                        msg.SenderEmailAddress,
                        msg.Subject,
                        os.path.basename(caminho),
                        xml
                    ))
                    conn.commit()
                    xml_processados += 1
                    print("XML inserido no Oracle")

        # move email se encontrou XML
        if encontrou_xml:
            msg.Move(processados)
            print("Email movido para Processados")

        # opcional: marca como lido mesmo sem XML
        else:
            msg.UnRead = False

    except Exception as e:
        print("Erro ao processar email:", e)

# -------------------------------
# FINALIZA
# -------------------------------

cursor.close()
conn.close()

print("================================")
print("Emails analisados:", total_emails)
print("XML processados:", xml_processados)
print("Processamento finalizado")
print("================================")
