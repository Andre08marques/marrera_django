import requests

import os
# importar a biblioteca
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# adicionar essa tag para que nosso projeto encontre o .env
load_dotenv(os.path.join(BASE_DIR, ".env"))


def autenticar():
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'app_id': os.getenv('cobrefacil_appid'),
        'secret': os.getenv('cobrefacil_secret'),
    }

    response = requests.post('https://api.cobrefacil.com.br/v1/authenticate', headers=headers, json=json_data)
    data = (response.json())
    return data['data']['token']

def cadastrar_cliente(body, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    type_cliente = body['cpf_cnpj']
    if type_cliente == "1":
        oclient = 'taxpayer_id'
        typofname = 'personal_name'
    else:
        oclient = 'ein'
        typofname = 'company_name'
        
    json_data = {
        'person_type': type_cliente,
        f'{oclient}': body['cpfCnpj'],
        f'{typofname}': body['nome'],
        'telephone': body['celular'],
        'cellular': body['celular'],
        'email': body['email'],
        'address': {
            'description': body['descricaoEndereco'],
            'zipcode': body['cep'],
            'street':  body['descricaoEndereco'],
            'number': body['numero'],
            'complement': body['complemento'],
            'neighborhood': body['bairro'],
            'city': body['cidade'],
            'state': body['estado'],
        },
    }
    response = requests.post('https://api.cobrefacil.com.br/v1/customers', headers=headers, json=json_data)
    data = (response.json())
    return data



def gerar_faturar(token, customer_id,  duedate, price):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    json_data = {
        'payable_with': "pix,bankslip,credit",
        'customer_id': f'{customer_id}',
        'due_date': f'{duedate}',
        'items': [
            {
                'description': 'mensalidade',
                'quantity': 1,
                'price': f"{price}"
            },
        ],
        'settings': {
            "send_tax_invoice": 1,
            'warning': {
                'description': '- Em caso de dúvidas entre em contato com nossa Central de Atendimento.',
            
            },
        },
    }
    response = requests.post('https://api.cobrefacil.com.br/v1/invoices', headers=headers, json=json_data)
    data = (response.json())
    return (data)


