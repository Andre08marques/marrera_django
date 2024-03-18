import requests

def get_all_grupos(key):
    url = f"https://apiwpp.marrera.net/group/fetchAllGroups/{key}?getParticipants=false"
    payload = {}
    headers = {
    'apikey': f'{key}'
    }
    try:
        response = requests.get(url, timeout=10, headers=headers)
        data = (response.json())
        return (data)
    except requests.exceptions.Timeout:
        data = (response.json())
        return (data)

    

