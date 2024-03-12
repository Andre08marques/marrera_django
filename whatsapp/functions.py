import requests


def create_instance():
    hash = gerar_chave()
    headers = {
                'Content-Type': 'application/json',
                'apikey': '62ce3b0f-6604-4df8-bbda-8707380a03fb'
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
                'apikey': '62ce3b0f-6604-4df8-bbda-8707380a03fb'
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
    



