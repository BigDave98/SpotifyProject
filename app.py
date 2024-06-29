from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = 'a1b2d3e4c5f6'
app.config['SESSION_COOKIE_NAME'] = 'Davis Cookie'

@app.route('/')
def login():
    sp_oauth = create_spotfy_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotfy_oauth()
    session.clear()
    return 'redirect'

@app.route('/getTracks')
def getTracks():
    return 'fkjnafkjna'

clientID = '07ea87a0e0c34aa28f6550d4d2f612dc'

clientSecret = '04bfced91d2349d49d0d840660ccb0ba'

def create_spotfy_oauth():
    return SpotifyOAuth(
        client_id='07ea87a0e0c34aa28f6550d4d2f612dc',
        client_secret='04bfced91d2349d49d0d840660ccb0ba',
        redirect_uri=url_for('redirectPage', _external = True),
        scope="user-library-read"
    )