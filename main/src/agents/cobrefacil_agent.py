from django.conf import settings
from main.src.httperro.http_erro import HttpErrors
import requests




class CobreFacil():

    def __init__(self):
        self.__base_url = settings.COBREFACIL_URL
        self.cobrefacil_appid = settings.COBREFACIL_APPID
        self.cobrefacil_secret = settings.COBREFACIL_SECRET

    
    def login(self):
        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'app_id': f'{self.cobrefacil_appid}',
            'secret': f'{self.cobrefacil_secret}',
        }
        response = requests.post(
            url=f"{self.__base_url}/authenticate",
            headers=headers,
            json=json_data
        )
      
        status_code = response.status_code
        if ((status_code >= 200) and (status_code <= 299)):
            data = {
                "status_code": response.status_code,
                "response": response.json()
            }
            return data['response']['data']['token']
        else: 
            raise HttpErrors(
                message=f'Erro ao tentar fazer login. {response.json()}',status_code=status_code
            )
        
    def create_client(self, token, data):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        
        if data.clienttype == '1':
                json_data = {
                    'person_type': 1,
                    'taxpayer_id': f'{data.cpfCnpj}',
                    'personal_name': f'{data.name}',
                    'cellular': f'{data.mobilePhone}',
                    'email': f'{data.email}',
                    'address': {
                        'description': f'principal',
                        'zipcode': f'{data.postalCode}',
                        'street': f'{data.address}',
                        'number': f'{data.addressNumber}',
                        'complement': f'{data.complement}',
                        'neighborhood': f'{data.district}',
                        'city': f'{data.city}',
                        'state': f'{data.state}',
                    },
                }
        else:
            json_data = {
                    'person_type': '2',
                    'ein': f'{data.cpfCnpj}',
                    'personal_name': f'{data.nome}',
                    'cellular': f'{data.mobilePhone}',
                    'email': f'{data.email}',
                    'address': {
                        'description': f'principal',
                        'zipcode': f'{data.postalCode}',
                        'street': f'{data.address}',
                        'number': f'{data.addressNumber}',
                        'complement': f'{data.complement}',
                        'neighborhood': f'{data.district}',
                        'city': f'{data.city}',
                        'state': f'{data.state}',
                    },
                }

        response = requests.post(
            url=f"{self.__base_url}/customers",
            headers=headers,
            json=json_data
        )
      
        status_code = response.status_code
        if ((status_code >= 200) and (status_code <= 299)):
            data = {
                "status_code": response.status_code,
                "response": response.json()
            }
            return data
        else: 
            raise HttpErrors(
                message=f'Erro ao tentar criar o cliente. Erro:{response.json()}',status_code=status_code
            )