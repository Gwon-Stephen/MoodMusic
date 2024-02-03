import requests, json


BASE_ADDRESS = "https://api.spotify.com"
headers = {
    "Accept": "application/json",
    'Content-Type': 'application/json',
    'Authorization': "Bearer "
  }


def request_user_spotify_id(access_token):
    headers['Authorization'] = "Bearer " + access_token
    response = requests.get(url = BASE_ADDRESS + "/v1/me", headers=headers)
    try:
        return response.json()['id']
    except:
        return({'Error': 'Retriving user failed'})


def request_user_display_name(user_id, access_token):
    headers['Authorization'] = "Bearer " + access_token
    response = requests.get(url = BASE_ADDRESS + "/v1/me", headers=headers)
    try:
        return response.json()['display_name']
    except:
        return({'Error': 'Retriving user failed'})
    

def make_API_call(access_token, endpoint, params='', data='', post=False, put=False):
    headers['Authorization'] = "Bearer " + access_token
    if post:
       response = requests.post(url = BASE_ADDRESS + endpoint, headers=headers, params=params, data=data)
    if put:
        response = requests.put(url = BASE_ADDRESS + endpoint, headers=headers, params=params)
    
    if not post and not put: 
        response = requests.get(url = BASE_ADDRESS + endpoint, headers=headers, params=params)
    try:
        return response.json()
    except:
        return({'Error': 'API call failed'})
