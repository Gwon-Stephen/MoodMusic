# additional webscraper method to help us identify which songs correlate with which emotions

def webscraper(access_token):
    import csv
    with open('data/songdata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["mood", "acousticness", "danceability", "energy", "instrumentalness", "key", "mode", "tempo", "valence"]
        writer.writerow(field)

        angry_uri_list = []
        angry_playlist_ids = ["37i9dQZF1EIhuCNl2WSFYd", "37i9dQZF1EIgNZCaOGb0Mi"]

        for playlist_id in angry_playlist_ids:
            endpoint = "/v1/playlists/" + playlist_id + "/tracks"
            parameters = {"fields":"items.track.id"}
            uris = make_API_call(access_token=access_token, endpoint=endpoint, params=parameters)['items']
            for u in uris:
                angry_uri_list.append(u['track']['id'])
        
        for uri in angry_uri_list:
            endpoint = "/v1/audio-features/" + uri 
            features = make_API_call(access_token=access_token, endpoint=endpoint)
            writer.writerow(["angry", features["acousticness"], features["danceability"], features["energy"], 
                             features["instrumentalness"], features["key"], features["mode"], features["tempo"], features["valence"]])
        
        print("angry done)")

        happy_uri_list = []
        happy_playlist_ids = ["37i9dQZF1EIgG2NEOhqsD7", "37i9dQZF1EIfAiavURxjpo"]

        for playlist_id in happy_playlist_ids:
            endpoint = "/v1/playlists/" + playlist_id + "/tracks"
            parameters = {"fields":"items.track.id"}
            uris = make_API_call(access_token=access_token, endpoint=endpoint, params=parameters)['items']
            for u in uris:
                happy_uri_list.append(u['track']['id'])
        
        for uri in happy_uri_list:
            endpoint = "/v1/audio-features/" + uri 
            features = make_API_call(access_token=access_token, endpoint=endpoint)
            writer.writerow(["happy", features["acousticness"], features["danceability"], features["energy"], 
                             features["instrumentalness"], features["key"], features["mode"], features["tempo"], features["valence"]])
        
        sad_uri_list = []
        sad_playlist_ids = ["37i9dQZF1EIdChYeHNDfK5", "37i9dQZF1EIh4v230xvJvd"]

        for playlist_id in sad_playlist_ids:
            endpoint = "/v1/playlists/" + playlist_id + "/tracks"
            parameters = {"fields":"items.track.id"}
            uris = make_API_call(access_token=access_token, endpoint=endpoint, params=parameters)['items']
            for u in uris:
                sad_uri_list.append(u['track']['id'])
        
        for uri in sad_uri_list:
            endpoint = "/v1/audio-features/" + uri 
            features = make_API_call(access_token=access_token, endpoint=endpoint)
            writer.writerow(["sad", features["acousticness"], features["danceability"], features["energy"], 
                             features["instrumentalness"], features["key"], features["mode"], features["tempo"], features["valence"]])
        
        neutral_uri_list = []
        neutral_playlist_ids = ["37i9dQZF1EVHGWrwldPRtj", "6IKQrtMc4c00YzONcUt7QH"]

        for playlist_id in neutral_playlist_ids:
            endpoint = "/v1/playlists/" + playlist_id + "/tracks"
            parameters = {"fields":"items.track.id"}
            uris = make_API_call(access_token=access_token, endpoint=endpoint, params=parameters)['items']
            for u in uris:
                neutral_uri_list.append(u['track']['id'])
        
        for uri in neutral_uri_list:
            endpoint = "/v1/audio-features/" + uri 
            features = make_API_call(access_token=access_token, endpoint=endpoint)
            writer.writerow(["neutral", features["acousticness"], features["danceability"], features["energy"], 
                             features["instrumentalness"], features["key"], features["mode"], features["tempo"], features["valence"]])
        