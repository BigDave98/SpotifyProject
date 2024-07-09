# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, jsonify, make_response
from utils.spotify import *


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
    return redirect(url_for('get_all_tracks', _external = True)) #redirect(url_for('index'))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get_all_tracks', methods = ['GET'])
def get_all_tracks():
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = make_response(
        jsonify(
            get_tracks(sp)
        )
    )
    return results

@app.route('/submit_selected_songs', methods=['POST'])
def submit_selected_songs():
    selected_songs = request.json
    path = "Data/selected_songs.csv"
    save_songs_csv(selected_songs, path)
    # Aqui você pode processar os itens selecionados como desejado
    print("Selected Songs:", selected_songs)
    return jsonify({'message': 'Selected songs received'}), 200

if __name__ == '__main__':
    app.run()