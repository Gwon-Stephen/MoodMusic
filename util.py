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
    parameters["limit"] = 10
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
    
    add_queue(access_token=access_token, songs=recommendations)
    return recommendations


def make_parameters(mood):
    parameters = {}
    if mood == 'happy':
        parameters["target_valence"] = 0.8
        parameters["target_danceability"] = 0.7260
        parameters["target_energy"] = 0.8
        parameters["target_mode"] = 1
    if mood == 'sad':
        parameters["target_acousticness"] = 0.7540
        parameters["target_danceability"] = 0.4035
        parameters["target_valence"] = 0.2070
        parameters["target_energy"] = 0.25
        parameters["target_mode"] = 0
    if mood == 'angry':
        parameters["max_acousticness"] = 0.0609
        parameters["target_instrumentalness"] = 0
        parameters["max_valence"] = 0.3
        parameters["min_energy"] = 0.5
        parameters["target_danceability"] = 0.75
        parameters["target_mode"] = 1
    if mood == 'neutral':
        parameters["target_instrumentalness"] = 0.0173
        parameters["target_danceability"] = 0.6910
        parameters["target_valence"] = 0.3270
        parameters["target_tempo"] = 115.939
        parameters["max_energy"] = 0.6
    print(parameters)
    return parameters

# takes list of Song objects & add songs to queue
def add_queue(access_token, songs):
    endpoint = "/v1/me/player/queue"
    parameters = {}
    print("adding to queue")
    for song in songs:
        print("adding", song.uri, "to queue")
        parameters["uri"] = song.uri
        make_API_call(access_token=access_token, endpoint=endpoint, params=parameters, post=True)
    endpoint = "/v1/me/player/next"
    make_API_call(access_token=access_token, endpoint=endpoint, post=True)


def make_playlist(access_token, mood, songs):
    spotify_id = request_user_spotify_id(access_token=access_token)
    endpoint = "/v1/users/" + spotify_id + "/playlists"
    data = json.dumps({
        "name": mood,
        "description": "AMPLIFY YOUR MOOD!",
        "public": True
    })
    playlist = make_API_call(access_token=access_token, endpoint=endpoint, data=data, post=True)["id"]
    
    endpoint = "/v1/playlists/" + playlist + "/tracks"
    uris = []
    for song in songs:
        uris.append(song.uri)

    data = json.dumps({
        "uris":uris
    })
    print(uris)
    return make_API_call(access_token=access_token, endpoint=endpoint, data=data, post=True)

def format_mood(mood):
    moodstring = ""
    if mood == 'happy':
        moodstring = "happy! :D"
    if mood == 'sad':
        moodstring = "down :()"
    if mood == 'angry':
        moodstring = "angry >:()"
    if mood == 'neutral':
        moodstring = "calm :)"
    return moodstring

# access OpenCV capture in frontend
# refresh page functionality 
