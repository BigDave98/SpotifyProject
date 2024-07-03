import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect
import time
import pandas as pd
import functions

app = Flask(__name__)

app.secret_key = 'a1b2d3e4c5f6'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('get_all_tracks', _external = True))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/get_all_tracks')
def get_all_tracks():
    session['token_info'] = get_token()
    session.modified = True
    #if not authorized:
    #    return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0

    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            results += [val]

        if (len(curGroup) < 50):
            break

    return results


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get(TOKEN_INFO, {})
    if not (session.get('token_info', False)):
        token_valid = False
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='07ea87a0e0c34aa28f6550d4d2f612dc',
        client_secret='04bfced91d2349d49d0d840660ccb0ba',
        redirect_uri=url_for('authorize', _external = True),
        scope="user-library-read"
    )



if __name__ == '__main__':
    app.run(debug=True)