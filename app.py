import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect
import json
import time
import pandas as pd
from downloadvideos import DownloadVideosFromTitles

app = Flask(__name__)

app.secret_key = 'a1b2d3e4c5f6'
app.config['SESSION_COOKIE_NAME'] = 'Davis Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotfy_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotfy_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external = True))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


def get_all_tracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
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

    df = pd.DataFrame(results, columns=["song names"])
    df.to_csv('songs.csv', index=False)
    return "done"

    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset= iter * 50)['items']
        iter += 1
        all_songs += items
        if len(items) < 50:
            break

    return str(all_songs)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotfy_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotfy_oauth():
    return SpotifyOAuth(
        client_id='07ea87a0e0c34aa28f6550d4d2f612dc',
        client_secret='04bfced91d2349d49d0d840660ccb0ba',
        redirect_uri=url_for('redirectPage', _external = True),
        scope="user-library-read"
    )