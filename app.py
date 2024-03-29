from flask import render_template, Flask, redirect, session, request
import requests, json, base64, cv2
import util, webscraper, mood
import numpy as np
from deepface import DeepFace

app = Flask(__name__)
app.secret_key = 'dev'

scopes = "ugc-image-upload playlist-modify-private playlist-modify-public user-top-read streaming user-modify-playback-state"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
CLIENT_ID = "1fc86b53f4fe4e91a95be7633ceb9782"
CLIENT_SECRET = "f4d40afac9e147298c9f9dd2ddab2b3d"

@app.route("/auth")
def auth():
    oauth = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scopes,
    }
    url = requests.get('https://accounts.spotify.com/authorize', oauth).url
    return redirect(url)
    
@app.route('/callback')
def callback():
    code = request.args.get('code')

    # get access token
    params = {
             'grant_type': "authorization_code",
             'code': code,
             'redirect_uri': REDIRECT_URI
        }
    credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')
    headers = {
             'Authorization': 'Basic ' + base64.b64encode(credentials).decode('utf-8'),
             'content-type': 'application/x-www-form-urlencoded',
         }
    token_full = requests.post("https://accounts.spotify.com/api/token", params=params, headers=headers).json()
    session["token"] = token_full['access_token']
    print(session["token"])
    session["user_id"] = util.request_user_spotify_id(session["token"])
    print(session["user_id"])

    #webscraper.webscraper(session["token"])
    return redirect("/results")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    model = DeepFace.build_model("Emotion")

    curmood = mood.getMood(face_cascade, model)
    session["name"] = util.request_user_display_name(session["token"])
    print(session["name"])
    session["mood"] = util.format_mood(curmood)

    recommendations = util.make_recommendations(access_token=session["token"], parameters=util.make_parameters(curmood))
    #recommendations = util.make_recommendations(access_token=session["token"], parameters=util.make_parameters("angry"))

    session["recommendations"] = []
    for song in recommendations:
        x = {
            "name": song.name,
            "artist": song.artist,
            "uri": song.uri,
            "cover-url": song.cover_url,
        }
        session["recommendations"].append(json.dumps(x))
    return (render_template('results.html', name=session["name"], mood=session["mood"], tracks=recommendations))

@app.route('/playlist')
def playlist():
    recommendations = []
    for song in session["recommendations"]:
        song = json.loads(song)
        s = util.Song(name=song["name"], artist=song["artist"], uri=song["uri"], cover_url=song["cover-url"])
        recommendations.append(s)
    
    #return (render_template('results.html', name=session["name"], mood=session["mood"], tracks=recommendations)) 
    url = util.make_playlist(access_token=session["token"], mood=session["mood"], songs=recommendations)
    return redirect(url)

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)