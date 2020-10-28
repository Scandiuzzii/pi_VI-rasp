from pi.mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def ler():
    try:
        id, text = reader.read()
        return id,text
    except Exception as e:
        raise e