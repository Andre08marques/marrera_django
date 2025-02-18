import requests
from main.src.httperro.http_erro import HttpErrors
from django.conf import settings



class AsaasAPI:

    def __init__(self):
        self.__base_url = settings.ASAAS_URL
        self.__asaas_key = settings.ASAAS_KEY
    
    def list_client(self, cpfCnpj):
          headers = {
          "accept": "application/json",
          "access_token": f"{self.__asaas_key}"
          }
          
          status_code = response.status_code
          if ((status_code >= 200) and (status_code <= 299)):
                response = requests.get(
                    headers=headers,
                    url=f'{self.__base_url}customers?cpfCnpj={cpfCnpj}'
                )
                return response.json()
          else: 
                raise HttpErrors(
                    message=response.json(), status_code=status_code
                )
        
    

    def get_client(self,id):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access_token": f"{self.__asaas_key}"
        }

        response = requests.post(
             headers=headers,
             url=f'{self.__base_url}customers/{id}'
             )

        return response.json()
    
    def create_client(self, name,cpf,email):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access_token": f"{self.__asaas_key}"
        }
        
        json = {
             "name": f"{name}",
             "cpfCnpj": f"{cpf}",
             "email": f"{email}"
        }
        
        status_code = response.status_code
        if ((status_code >= 200) and (status_code <= 299)):
            response = requests.post(
                headers=headers,
                json=json,
                url=f'{self.__base_url}customers'
                )

            return response.json()
        else: 
            raise HttpErrors(
                message=response.json(), status_code=status_code
            )