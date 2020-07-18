import requests

url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create"

headers = {
    'accept': "application/json",
    'authorization': "Authorization",
    'x-app-key': "X-APP-Key",
    'content-type': "application/json"
    }

response = requests.request("POST", url, headers=headers)

print(response.text)