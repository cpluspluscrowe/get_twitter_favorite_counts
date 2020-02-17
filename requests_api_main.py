import requests

def get_keys():
    with open("keys.org") as f:
        k,v = f.read().split("\n")[:2]
        return (k,v)

# Get a status of 200 to show the requests work
    
client_key, client_secret = get_keys()
import base64
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'

auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# Now use the response to get the access token
access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}
search_params = {
    'q': 'NASA',
    'result_type': 'recent',
    'count': 2
}
search_url = '{}1.1/search/tweets.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers, params=search_params)

import json 
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}
search_params = {
    'q': 'NASA',
    'result_type': 'recent',
    'count': 10
}
search_url = '{}1.1/search/tweets.json'.format(base_url)# Execute the get request
search_resp = requests.get(search_url, headers=search_headers, params=search_params)# Get the data from the request
Data = json.loads( search_resp.content )# Print out the data!
print(Data['statuses'])
