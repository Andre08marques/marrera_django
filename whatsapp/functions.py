import requests
# importar a biblioteca
from dotenv import load_dotenv
import os



def create_instance():
    hash = gerar_chave()
    headers = {
                'Content-Type': 'application/json',
                'apikey': os.getenv('evolutionapikey')
            }
    json_data = {
                        "instanceName": f"{hash}",
                        "qrcode": False,
                        "token": f"{hash}"

                        
                    }
                                        
                

    response = requests.post('https://apiwpp.marrera.net/instance/create', headers=headers, json=json_data)
    data = (response.json())
    return data

def instance_connect(apikey, nome):
    headers = {
            'apikey': f'{apikey}'
            }

    response = requests.get(f'https://apiwpp.marrera.net/instance/connect/{nome}', headers=headers)
    data = (response.json())
    return (data)


def instance_desconect(apikey, nome):
    headers = {
            'apikey': f'{apikey}'
            }

    response = requests.delete(f'https://apiwpp.marrera.net/instance/logout/{nome}', headers=headers)
    data = (response.json())
    


#deletar instancia
def instance_delete(apikey, nome):
    headers = {
            'apikey': f'{apikey}'
            }

    response = requests.delete(f'https://apiwpp.marrera.net/instance/delete/{nome}', headers=headers)
    data = (response.json())


#pegar todas as intâncias criadas
def get_instances():
    headers = {
                'apikey': os.getenv('evolutionapikey')
            }
    
    try:
        response = requests.get("https://apiwpp.marrera.net/instance/fetchInstances", timeout=10, headers=headers)
        data = (response.json())
        return (data)
    except requests.exceptions.Timeout:
        return ("timeout")
    
#gerar token aleatório
import string
import random

def gerar_chave(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    



