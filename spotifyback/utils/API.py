from spotipy.oauth2 import SpotifyOAuth
from flask import url_for
import time
import os
from spotify import save_songs_csv

#This file contais every code that acctualy calls the Spotify API
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('authorize', _external = True),
        scope="user-library-read"
    )

#Get the Liked songs List
def get_tracks(sp, path):
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

    save_songs_csv(results, path)
    return results

# Checks to see if token is valid and gets a new token if not
def get_token(session):
    token_info = session.get("token_info", {})
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_expired = session.get('token_info').get('expires_at') - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid