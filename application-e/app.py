from flask import Flask, session, redirect, request, render_template
import requests
import os
import jwt

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

KEYCLOAK_URL = "http://keycloak:8080"  # URL interne à Docker
CLIENT_ID = "application-e" #A changer avec le nom du client keycloak
CLIENT_SECRET = "myclient-secret" #A changer avec le secret du client keycloak
REALM_NAME = "myrealm"
PROXY_URL = "http://user/app" # URL du reverse proxy

@app.route('/')
def index():
    if 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        try:
            response = requests.get("http://localhost:5000/protected", headers=headers) #Appel interne, on utilise le nom du service
            response.raise_for_status()
            return render_template('index.html', content=response.text)
        except requests.exceptions.RequestException as e:
            return f"Erreur lors de l'appel à /protected: {e}"
    else:
        return render_template('index.html', content="Non connecté. <a href='/login'>Se connecter</a>")

@app.route('/login')
def login():
    authorization_url = f"{KEYCLOAK_URL}/realms//{REALM_NAME}/protocol/openid-connect/auth"
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
    token_url = f"http://keycloak:8080/realms/{REALM_NAME}/protocol/openid-connect/token"
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

    # Décoder le jeton d'accès
    try:
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        return f"Jeton d'accès décodé: {decoded_token}"
    except Exception as e:
        return f"Erreur lors du décodage du jeton d'accès: {e}"

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect('/')

@app.route('/protected')
def protected():
    # Cette route est protégée et ne devrait être accessible qu'avec un token valide.
    return "Contenu protégé! Vous êtes authentifié."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
