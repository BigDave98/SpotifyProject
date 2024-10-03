# -*- coding: utf-8 -*-
import spotipy
from flask import Flask, render_template, redirect, session
from utils.spotify import *
from utils.DownloadVideos import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = os.getenv("SESSION_COOKIE_NAME")
TOKEN_INFO = os.getenv("TOKEN_INFO")

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
    return redirect(url_for('get_all_tracks', _external=True))  # redirect(url_for('index'))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get_all_tracks')
def get_all_tracks():
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    path = 'Data\songs.csv'
    all_tracks = tracks(path, sp)

    search_query = request.args.get('search', '', type=str)

    # Aplicar filtro se houver um termo de pesquisa
    if search_query:
        all_tracks = [track for track in all_tracks if search_query in track]
        print(all_tracks)

    return pagination(all_tracks)

@app.route('/submit_selected_songs', methods=['POST'])
def submit_selected_songs():
    selected_songs = request.json.get('selectedSongs', [])

    path = "Data/selected_songs.csv"
    save_songs_csv(selected_songs, path)
    return video_dowload(selected_songs)


if __name__ == '__main__':
    app.run()