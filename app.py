from flask import render_template, Flask, redirect
import requests, json, base64

app = Flask(__name__)
app.secret_key = 'dev'

scopes = "ugc-image-upload playlist-modify-private playlist-modify-public user-top-read"
REDIRECT_URI = "http://127.0.0.1:5000/callback"

@app.route("/auth")
def auth():
    oauth = {
        'client_id': "602926a561c04ccc83591ca0a422e50f",
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scopes,
    }
    url = requests.get('https://accounts.spotify.com/authorize', oauth).url
    return redirect(url)
    
@app.route('/callback')
def callback():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)