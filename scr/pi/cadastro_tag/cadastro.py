import requests
from config import Config

conf = Config()

def cadastrar(tag):
    payload = {
        'tag' : tag
    }
    try:
        requests.post(str(conf.HOST) + '/tag/',json=payload)
        
    except Exception as e :
        raise e
