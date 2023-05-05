import requests
import os 

def retrieve_token():
    api_key = os.environ.get('flight_api_key')
    api_secret = os.environ.get('flight_api_secret')
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    payload = "grant_type=client_credentials&client_id={}&client_secret={}".format(api_key,api_secret)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)
    return (response.json()['access_token'])


if __name__ == "__main__":
    retrieve_token()

