from django.conf import settings
from main.src.httperro.http_erro import HttpErrors
import requests
import string
import random



def gerar_chave(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Evolution():

    def __init__(self):
        self.__base_url = settings.EVOLUTION_API_URL
        self.__evolutionmasterkey = settings.EVOLUTIONMASTERKEY
        
    
    def instance_create(self, name):
        try:
            json = {
                "token": f"{self.__evolutionmasterkey}",
                "groups_ignore": "false",
            }
            
            response = requests.post(
                url=f"{self.__base_url}/instance",
                json=json
            )
            response.raise_for_status() 
                    
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
    
    def instance_recreate(self, name, key):
        try:
            headers = {
                "apikey": f"{self.__evolutionmasterkey}"
            }

            json = {
                "token": f"{self.__evolutionmasterkey}",
                "groups_ignore": "false",
            }
            
            response = requests.post(
                url=f"{self.__base_url}/instance",
                headers=headers,
                json=json,
                timeout=15  
            )
            response.raise_for_status() 
            
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
        
        
       
            
    
    def instance_status(self, name, key):
        try:
            headers = {
                "apikey": f"{key}"
            }

            response = requests.get(
                    url=f"{self.__base_url}/instance/state/{name}",
                    headers=headers,
                )
            
            response.raise_for_status() 
                
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
    

    def instance_connect(self, name, key):
        try:
            headers = {
                "apikey": f"{key}"
            }
            
            response = requests.get(
                    url=f"{self.__base_url}/instance/{name}",
                    headers=headers,
                )
            
            response.raise_for_status() 
                    
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
    
    def instance_desconect(self, name, key):
        try:
            headers = {
                "apikey": f"{key}"
            }

            response = requests.put(
                    url=f"{self.__base_url}/instance/logout/{name}",
                    headers=headers,
                )
            
            response.raise_for_status() 
                        
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
    
    def instance_delete(self, name, key):
        try:
            headers = {
                "apikey": f"{key}"
            }
            json = {
                "token": "{{token}}"
            }

            response = requests.delete(
                    url=f"{self.__base_url}/instance/{name}",
                    headers=headers,
                    json=json
                )
            
            response.raise_for_status() 
                        
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
    
    def instance_send_text(self, name, key, number, text):
        try:
            headers = {
                "apikey": f"{key}"
            }

            json = {
                "number": f'{number}',
                "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": "false"
                },
                "textMessage": {
                    "text": f"{text}"
                }
            }
            
            response = requests.post(
                url=f"{self.__base_url}/message/sendText/{name}",
                headers=headers,
                json=json
            )
            response.raise_for_status() 
                        
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
    
    def instance_send_media(self, name, key, number, text, media_url):
        try:
            headers = {
                "apikey": f"{key}"
            }

            json =  {
                        "number": f"{number}",
                        "options": {
                            "delay": 1200,
                            "presence": "composing"
                        },
                        "mediaMessage": {
                            "mediatype": "image",
                            "caption": f"{text}",
                            "media": f"{media_url}"
                        }
                    }
            
            response = requests.post(
                url=f"{self.__base_url}/message/sendMedia/{name}",
                headers=headers,
                json=json
            )
            response.raise_for_status() 
                        
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)
        
    def instance_get_group(self, name, key):
        try:
            headers = {
                "apikey": f"{key}"
            }

            response = requests.get(
                    url=f"{self.__base_url}/group/fetchAllGroups/{name}?getParticipants=false",
                    headers=headers,
                )
            
            response.raise_for_status() 
                        
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.Timeout:
            raise HttpErrors(message="A requisição expirou. O servidor pode estar indisponível.", status_code=504)
        
        except requests.exceptions.ConnectionError:
            raise HttpErrors(message="Erro de conexão com a API. O servidor pode estar fora do ar.", status_code=503)

        except requests.exceptions.HTTPError as e:
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = "Erro desconhecido na API"
            raise HttpErrors(message=error_response, status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            raise HttpErrors(message=f"Erro na requisição: {str(e)}", status_code=500)


