# importar a biblioteca
import requests
from dotenv import load_dotenv
import os

def get_all_grupos(key):
    url = f"https://apiwpp.marrera.net/group/fetchAllGroups/{key}?getParticipants=false"
    payload = {}
    headers = {
    'apikey': f'{key}'
    }

    response = requests.get(url,headers=headers, timeout=15)
    data = (response)
    return (data)
