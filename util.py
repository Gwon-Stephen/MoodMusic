import requests, json

BASE_ADDRESS = "https://api.spotify.com"
headers = {
    "Accept": "application/json",
    'Content-Type': 'application/json',
    'Authorization': "Bearer "
  }

class Song:
    def __init__(self, name, artist, uri, cover_url):
        self.name = name
        self.artist = artist
        self.uri = uri
        self.cover_url = cover_url

# Spotify ID
def request_user_spotify_id(access_token):
    headers['Authorization'] = "Bearer " + access_token
    response = requests.get(url = BASE_ADDRESS + "/v1/me", headers=headers)
    try:
        return response.json()['id']
    except:
        return({'Error': 'Retriving user failed'})

# Display Name
def request_user_display_name(access_token):
    headers['Authorization'] = "Bearer " + access_token
    response = requests.get(url = BASE_ADDRESS + "/v1/me", headers=headers)
    try:
        return response.json()['display_name']
    except:
        return({'Error': 'Retriving user failed'})
    
# catch all method for making Spotify API calls
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

# return a list of Song objects
def make_recommendations(access_token, parameters):
    # First we will take into consideration base user preferences: 
    # get top 2 artists
    endpoint = "/v1/me/top/artists"
    
    artists = make_API_call(access_token=access_token, endpoint=endpoint)["items"][0]['id'] + "," + make_API_call(access_token
        =access_token, endpoint=endpoint)["items"][1]['id']
    
    # get top 3 tracks
    endpoint = "/v1/me/top/tracks"
    tracks = make_API_call(access_token=access_token, endpoint=endpoint)["items"][1]['id'] + "," + make_API_call(access_token
            =access_token, endpoint=endpoint)["items"][1]['id'] + "," + make_API_call(access_token=
            access_token, endpoint=endpoint)["items"][2]['id']
    
    # get recommendations
    parameters["seed_artists"] = artists
    parameters["seed_tracks"] = tracks
    endpoint = "/v1/recommendations"
    response = make_API_call(access_token=access_token, endpoint=endpoint, params=parameters)["tracks"]
    
    # clean recommendations and return as array of Song objects
    recommendations = []
    for track in response:
        name = track["name"]
        artists = []
        for artist in track["artists"]:
            artists.append(artist["name"])
        uri = track["uri"]
        url = track["album"]["images"][0]["url"]
        song = Song(name=name, artist=', '.join(artists), uri=uri, cover_url=url)
        recommendations.append(song)
    return recommendations


def make_parameters(mood):
    parameters = {}

    if (mood == 'happy'):
        parameters["valence"] = 0
    
    return parameters

# takes list of Song objects & add songs to queue
def add_queue(access_token, songs):
    # clear queue 
    return 0


# write openCV image to static files & access in frontend
