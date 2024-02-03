from flask import render_template, Flask, redirect, session, request
import requests, json, base64
import util

app = Flask(__name__)
app.secret_key = 'dev'

scopes = "ugc-image-upload playlist-modify-private playlist-modify-public user-top-read"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
CLIENT_ID = "602926a561c04ccc83591ca0a422e50f"
CLIENT_SECRET = "9ba1ef576668404285679f387eb13783"

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
    session["user_id"] = util.request_user_spotify_id(session["token"])
    return redirect("/results")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    print( session["user_id"])
    return (render_template('index.html'))

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)