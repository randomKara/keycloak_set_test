from flask import Flask, session, redirect, request
from authlib.integrations.flask_client import OAuth
import os
from functools import wraps
import jwt


app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth = OAuth(app)

keycloak = oauth.register(
    name='keycloak',
    server_metadata_url=f'{os.getenv("KEYCLOAK_URL")}/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration',
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    client_kwargs={'scope': 'openid profile roles'},
)

def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if session.get('user'):
               if role:
                   user_roles = session['user'].get('roles',[])
                   if role not in user_roles:
                          return "Unauthorized", 403
               return fn(*args, **kwargs)
            return redirect('/login')
        return decorated_view
    return wrapper

@app.route('/')
@login_required(role='admin')
def home():
    return f'Bonjour Admin {session["user"]["name"]} ! Vous êtes connecté à l\'application B'


@app.route('/login')
def login():
    redirect_uri = request.base_url.replace('/login', '/callback')
    return keycloak.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = keycloak.authorize_access_token()
    user_info = token.get('userinfo')
    access_token = token.get('access_token')
    decoded_token = jwt.decode(access_token, options={"verify_signature": False})
    roles = decoded_token.get('realm_access').get('roles')
    session['user'] = {
        'name': user_info.get('name', 'User'),
        'roles': roles
    }
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)