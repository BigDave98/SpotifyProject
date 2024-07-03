from flask import Flask, render_template, redirect, request, url_for

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
    return redirect(url_for('get_all_tracks', _external = True))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/get_all_tracks')
def get_all_tracks():
    session['token_info'] = get_token(TOKEN_INFO)
    session.modified = True
    results = get_tracks(session)
    return render_template('index.html', songs = results)

if __name__ == '__main__':
    app.run(debug=True)