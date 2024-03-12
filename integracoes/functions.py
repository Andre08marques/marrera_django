import requests

def ixc_sendtext(instanceName, recipientNumber, textMessage):
    url = f"http://172.30.131.6:3000/send-message/id={instanceName}"

    payload = {
        "number": f"{recipientNumber}",
        "textMessage": {"text": f"{textMessage}"}
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "insomnia/8.6.0"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    