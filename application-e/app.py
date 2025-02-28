from flask import Flask, session, redirect, request, render_template
import requests
import os
import jwt
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

KEYCLOAK_URL = "http://keycloak:8080"  # URL interne à Docker
CLIENT_ID = "application-e" #A changer avec le nom du client keycloak
CLIENT_SECRET = "myclient-secret" #A changer avec le secret du client keycloak
REALM_NAME = "myrealm"
PROXY_URL = "http://user/app" # URL du reverse proxy

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect('/app/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    access_token = session['access_token']
    try:
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        user_name = decoded_token.get('name', 'Utilisateur')  # Récupérer le nom de l'utilisateur
        return render_template('index.html', content=f"Bonjour {user_name} !")
    except Exception as e:
        return f"Erreur lors du décodage du jeton d'accès: {e}"

@app.route('/login')
def login():
    authorization_url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth" # ???? pourquoi deux "//" ?
    redirect_uri = PROXY_URL + "/callback"  # Utiliser l'URL du reverse proxy
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid',
        'redirect_uri': redirect_uri
    }
    auth_url = authorization_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    redirect_uri = PROXY_URL + "/callback"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()
    access_token = tokens['access_token']
    session['access_token'] = access_token  # Stocker le jeton dans la session
    return redirect('/app/')


@app.route('/protected')
@login_required
def protected():
    # Cette route est protégée et ne devrait être accessible qu'avec un token valide.
    return "Contenu protégé! Vous êtes authentifié."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
