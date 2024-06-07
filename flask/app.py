from flask import Flask, redirect, url_for, session, request, jsonify
import requests
import pkce
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

CLIENT_ID = 'ihfF8TmV2ggMuUgsbDEpDvSGvKG2xMT4T3qAhmHS'
CLIENT_SECRET = 'Pko6fQYlEIcg3CcLRe1mqqF2X5ZbcKBMExan42iAmQmJKpri1T35dYfoNbIHZo2UsdTAN0aL6BxIMvHgOGCRDv1jg2XXYBjA8n2jj4GEiLaMFBhx2w3kpyAWfo3AvMl3'
AUTHORIZATION_BASE_URL = 'http://localhost:8000/oauth/authorize/'
TOKEN_URL = 'http://localhost:8000/oauth/token/'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def home():
    return '''
        <h1>Flask OAuth Client</h1>
        <a href="/login">Login with OAuth</a>
    '''

@app.route('/login')
def login():
    code_verifier = pkce.generate_code_verifier(length=128)
    session['code_verifier'] = code_verifier
    code_challenge = pkce.get_code_challenge(code_verifier)

    authorization_url = f"{AUTHORIZATION_BASE_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&code_challenge={code_challenge}&code_challenge_method=S256"
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    print(session)
    error = request.args.get('error')
    if error:
        return f"Error: {error}"

    code = request.args.get('code')
    if not code:
        return 'Missing code parameter.'

    code_verifier = session.get('code_verifier')
    if not code_verifier:
        return 'Missing code verifier in session.'

    token_response = requests.post(TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code_verifier': code_verifier,
    })
    token_json = token_response.json()

    if 'error' in token_json:
        return f"Error: {token_json['error']} - {token_json.get('error_description')}"

    session['oauth_token'] = token_json['access_token']
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    token = session.get('oauth_token')
    if token is None:
        return redirect(url_for('login'))
    
    response = requests.get('http://localhost:8000/protected/', headers={
        'Authorization': f'Bearer {token}'
    })
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
