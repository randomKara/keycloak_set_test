Ce projet démontre une configuration multi-application utilisant Keycloak pour l'authentification et l'autorisation. Il inclut plusieurs applications (A, B, C, D et E), cinq reverse proxies (un pour l'application C, un pour l'application E, un pour l'administration de Keycloak, un pour l'application D et un pour une autre instance de Keycloak), un serveur Keycloak, un serveur Keycloak IDP et un proxy DNS, tous orchestrés avec Docker Compose.

## Aperçu

- **Keycloak:** Le serveur de gestion d'identité et d'accès.
- **Keycloak IDP:** Un serveur Keycloak servant de fournisseur d'identité (IDP).
- **Application A & B:** Applications Flask (Python) qui nécessitent une authentification utilisateur via Keycloak. L'application B nécessite le rôle "admin".
- **Application C:** Une application Flask (Python) qui affiche les informations de l'utilisateur extraites des en-têtes par le reverse proxy.
- **Application D:** Une application Flask (Python) qui utilise un client Keycloak spécifique et nécessite une authentification utilisateur via Keycloak.
- **Application E:** Une application Flask (Python) qui utilise une authentification manuelle via Keycloak.
- **Reverse Proxy (Application C):** Un serveur Apache agissant comme passerelle, authentifiant les requêtes via Keycloak et passant les informations de l'utilisateur dans les en-têtes à l'application C.
- **Reverse Proxy (Application E):** Un serveur Apache agissant comme passerelle pour l'application E.
- **Reverse Proxy (Administration Keycloak):** Un serveur Apache agissant comme passerelle pour l'administration de Keycloak.
- **Reverse Proxy (Application D):** Un serveur Apache agissant comme passerelle pour l'application D.
- **Reverse Proxy (Keycloak):** Un serveur Apache agissant comme passerelle pour une autre instance de Keycloak.
- **Proxy DNS:** Un serveur DNS pour la résolution de noms de domaine personnalisés à l'intérieur du réseau Docker.

## Fonctionnalités

- **Authentification centralisée:** Keycloak gère l'authentification des utilisateurs pour toutes les applications.
- **Contrôle d'accès basé sur les rôles:** L'application B n'est accessible qu'aux utilisateurs ayant le rôle "admin".
- **Single Sign-On (SSO):** Une fois authentifiés, les utilisateurs peuvent accéder aux applications sans se réauthentifier.
- **Authentification par Reverse Proxy:** Le reverse proxy gère l'authentification avant de transmettre les requêtes à l'application C ou D, en injectant les informations de l'utilisateur dans les en-têtes.
- **DNS personnalisé:** Le proxy DNS permet d'accéder aux services à l'intérieur du réseau Docker en utilisant des noms de domaine personnalisés comme `auth.test`.
- **Texte d'accueil configurable:** L'application A permet aux utilisateurs administrateurs de modifier le texte d'accueil affiché.
- **Authentification manuelle via Keycloak:** L'application E utilise une authentification manuelle via Keycloak.
- **Identity Provider (IDP) Brokerage:** Toutes les applications démontrent l'utilisation d'un IDP Keycloak pour l'authentification.

## Installation

1. **Cloner le projet:**

```shell
git clone https://github.com/randomKara/keycloak_set_test
```

2. **Se déplacer dans le répertoire du projet:**

```shell
cd keycloak_set_test/
```

3. **Lancer le projet en utilisant Docker Compose:**

```shell
docker-compose up --build
```

4. **Configuration DNS:** Ajouter le sous-réseau du projet à la configuration DNS de votre système. Ceci est requis pour que les reverses proxys fonctionnent correctement.

- **Non-Permanent:** Exécuter la commande suivante à chaque démarrage de votre PC.

```shell
sudo sed -i '2i nameserver 172.28.0.1' /etc/resolv.conf
```

## Utilisation

1. **Accéder à Keycloak:**

- Ouvrir votre navigateur web et naviguer vers `http://keycloak:8080`.
- Se connecter avec les identifiants administrateur par défaut:
    - **Nom d'utilisateur:** `admin`
    - **Mot de passe:** `admin`

2. **Accéder aux Applications:**

Voici un tableau récapitulatif des adresses IP et des ports pour chaque application :

| **Application**             | **URL d'accès**        |
| :---------------------------- | :---------------------- |
| Keycloak                    | `http://localhost:8080` |
| Keycloak à travers un RP     | `http://admin`          |
| Keycloak IDP                | `http://localhost:8081` |
| Application A               | `http://localhost:5000` |
| Application B               | `http://localhost:5001` |
| Application C               | `http://localhost:5002` |
| Application C derrière RP  | `http://auth.test:8085` |
| Application D               | `http://localhost:5003` |
| Application D derrière RP  | `http://rp-d`      |
| Application E               | `http://localhost:5004` |
| Application E à travers un RP | `http://user/app`        |

3. **Se connecter via Keycloak:**

- Lors de l'accès à l'application A, B ou D, vous serez redirigé vers Keycloak pour vous connecter.
- Se connecter en utilisant les identifiants suivants:
    - **Utilisateur:**
        - **Nom d'utilisateur:** `user`
        - **Mot de passe:** `user`
    - **Administrateur:**
        - **Nom d'utilisateur:** `admin`
        - **Mot de passe:** `admin`
- L'application B nécessite le rôle "admin"; connectez-vous donc avec l'utilisateur administrateur pour accéder à sa page d'accueil.
- La connection à Keycloak via le reverse proxy sur http://admin necessite d'utiliser le nom d'utilisateur "admin".

4. **Fonctionnalités des Applications:**

- **Application A:** Affiche un message de bienvenue. Si vous vous connectez avec l'utilisateur administrateur, un formulaire s'affiche, vous permettant de modifier le texte de bienvenue.
- **Application B:** Affiche un message de bienvenue spécifique si l'utilisateur a le rôle "admin".
- **Application C:** Affiche le nom et les rôles de l'utilisateur extraits des en-têtes par le reverse proxy.
- **Application D:** Affiche un message de bienvenue avec le nom de l'utilisateur connecté.
- **Application E:** Affiche le jeton d'accès décodé.
- **Reverse Proxy Admin:** Interface d'administration de Keycloak.
- **Reverse Proxy Keycloak (rp-k):** Reverse proxy de Keycloak.

## Architecture du Projet

### 1. Docker Compose (`docker-compose.yml`)

- Définit les services Docker et les configurations réseau.
- Gère les dépendances entre les conteneurs (par exemple, s'assurer que les applications démarrent après Keycloak).
- Configure les adresses IP statiques pour chaque conteneur sur le réseau `app-network`.

### 2. Keycloak

- Fournit des services d'authentification et d'autorisation centralisés.
- Gère les utilisateurs, les rôles et les clients (applications).
- Importe un realm préconfiguré à partir du dossier `keycloak/` au démarrage.

### 3. Keycloak IDP

- Fournit une instance Keycloak supplémentaire servant de fournisseur d'identité (IDP).
- Importe un realm préconfiguré à partir du dossier `idp/` au démarrage.

### 4. Applications

#### Application A (`application-a/`)

- **Fonctionnement :**
    1. L'utilisateur accède à l'application A (`http://localhost:5000`).
    2. L'application A redirige l'utilisateur vers Keycloak pour l'authentification via la route `/login` (application-a/app.py:49-52).
    3. Keycloak authentifie l'utilisateur (nom d'utilisateur et mot de passe).
    4. Keycloak redirige l'utilisateur vers l'application A avec un code d'autorisation via la route `/callback` (application-a/app.py:54-65).
    5. L'application A échange le code d'autorisation contre un jeton d'accès auprès de Keycloak.
    6. L'application A décode le jeton d'accès pour extraire les informations de l'utilisateur (nom, rôles).
    7. L'application A stocke les informations de l'utilisateur dans la session.
    8. L'application A affiche la page d'accueil avec un message de bienvenue personnalisé.
    9. Si l'utilisateur a le rôle "admin", un formulaire permettant de modifier le texte de bienvenue s'affiche.

- **Fichiers importants :**
    - `app.py` (application-a/app.py:1-73): Code principal de l'application Flask.
    - `templates/home.html`: Template HTML pour la page d'accueil.

#### Application B (`application-b/`)

- **Fonctionnement :**
    1. L'utilisateur accède à l'application B (`http://localhost:5001`).
    2. L'application B redirige l'utilisateur vers Keycloak pour l'authentification via la route `/login` (application-b/app.py:40-43).
    3. Keycloak authentifie l'utilisateur (nom d'utilisateur et mot de passe).
    4. Keycloak redirige l'utilisateur vers l'application B avec un code d'autorisation via la route `/callback` (application-b/app.py:45-56).
    5. L'application B échange le code d'autorisation contre un jeton d'accès auprès de Keycloak.
    6. L'application B décode le jeton d'accès pour extraire les informations de l'utilisateur (nom, rôles).
    7. L'application B stocke les informations de l'utilisateur dans la session.
    8. L'application B vérifie si l'utilisateur a le rôle "admin" (application-b/app.py:35).
    9. Si l'utilisateur a le rôle "admin", l'application B affiche la page d'accueil avec un message de bienvenue spécifique.
    10. Si l'utilisateur n'a pas le rôle "admin", l'application B affiche une erreur "Unauthorized".

- **Fichiers importants :**
    - `app.py` (application-b/app.py:1-56): Code principal de l'application Flask.

#### Application C (`application-c/`, `reverse-proxy/`)

- **Fonctionnement :**
    1. L'utilisateur accède au reverse proxy pour l'application C (`http://auth.test:8085`).
    2. Le reverse proxy vérifie si l'utilisateur est authentifié auprès de Keycloak.
    3. Si l'utilisateur n'est pas authentifié, le reverse proxy redirige l'utilisateur vers Keycloak pour l'authentification.
    4. Keycloak authentifie l'utilisateur (nom d'utilisateur et mot de passe).
    5. Keycloak redirige l'utilisateur vers le reverse proxy.
    6. Le reverse proxy extrait les informations de l'utilisateur (nom, rôles) du jeton d'accès fourni par Keycloak.
    7. Le reverse proxy transmet les informations de l'utilisateur à l'application C via les en-têtes HTTP (`X-User-Name`, `X-User-Roles`) (reverse-proxy/oidc.conf:24-25).
    8. L'application C reçoit la requête avec les en-têtes contenant les informations de l'utilisateur (application-c/app.py:9-10).
    9. L'application C affiche les informations de l'utilisateur.

- **Fichiers importants :**
    - `app.py` (application-c/app.py:1-12): Code principal de l'application Flask.
    - `templates/user_info.html`: Template HTML pour afficher les informations de l'utilisateur.
    - `reverse-proxy/proxy.conf`: Configuration Apache pour le reverse proxy.
    - `reverse-proxy/oidc.conf` (reverse-proxy/oidc.conf:1-30): Configuration OIDC pour le reverse proxy.

#### Application D (`application-d/`, `rp-d/`)

- **Fonctionnement :**
    1. L'utilisateur accède au reverse proxy pour l'application D (`http://rp-d`).
    2. Le reverse proxy vérifie si l'utilisateur est authentifié auprès du reverse proxy de Keycloak via `rp-k`.
    3. Si l'utilisateur n'est pas authentifié, le reverse proxy redirige l'utilisateur vers le reverse proxy de Keycloak pour l'authentification.
    4. Le reverse proxy de Keycloak authentifie l'utilisateur (nom d'utilisateur et mot de passe).
    5. Le reverse proxy de Keycloak redirige l'utilisateur vers le reverse proxy.
    6. Le reverse proxy de l'application D transmet les informations de l'utilisateur à l'application D via les en-têtes HTTP (`X-User-Name`).
    7. L'application D reçoit la requête avec les en-têtes contenant les informations de l'utilisateur.
    8. L'application D affiche les informations de l'utilisateur.

- **Points clés :**
    - Utilise un reverse proxy (`rp-d`) pour gérer l'authentification devant Keycloak.
    - Le reverse proxy (`rp-d`) s'appuie sur une autre instance Keycloak (`rp-k`) pour valider l'identité de l'utilisateur. Cela permet à ce que l'utilisateur ne soit jamais en contact direct avec Keycloak ou avec l'application D.
    - La configuration du client Keycloak (ID et secret) est spécifique à l'application D, permettant une gestion granulaire des autorisations.

- **Fichiers importants :**
    - `app.py` (application-d/app.py:1-14): Code principal de l'application Flask.
    - `templates/user_info.html`: Template HTML pour afficher les informations de l'utilisateur.
    - `rp-d/proxy.conf`: Configuration Apache pour le reverse proxy.
    - `rp-d/oidc.conf`: Configuration OIDC pour le reverse proxy.

#### Application E (`application-e/`, `reverse-proxy-user/`)

- **Fonctionnement :**
    1. L'utilisateur accède à l'application E via le reverse proxy (`http://user/app`).
    2. Si l'utilisateur n'est pas connecté, l'application E affiche un lien vers la page de connexion (`+/login`) (application-e/app.py:27).
    3. Lorsque l'utilisateur clique sur le lien de connexion, il est redirigé vers Keycloak en restant sur le reverse proxy pour l'authentification (application-e/app.py:30-40).
    4. Keycloak authentifie l'utilisateur (nom d'utilisateur et mot de passe).
    5. Keycloak redirige l'utilisateur vers l'application E avec un code d'autorisation via la route `/callback` (application-e/app.py:43-54).
    6. L'application E échange le code d'autorisation contre un jeton d'accès auprès de Keycloak.
    7. L'application E décode le jeton d'accès et affiche le jeton décodé (application-e/app.py:59-62).

- **Fichiers importants :**
    - `app.py` (application-e/app.py:1-74): Code principal de l'application Flask.
    - `templates/index.html` (application-e/templates/index.html:1-13): Template HTML pour la page d'accueil.
    - `reverse-proxy-user/conf/httpd.conf`: Configuration Apache pour le reverse proxy.
    - `reverse-proxy-user/conf/httpd-vhosts.conf` (reverse-proxy-user/conf/httpd-vhosts.conf:1-19): Virtual host configuration pour le reverse proxy.

#### Reverse Proxy Keycloak (rp-k) (`rp-k/`)

- **Fonctionnement :**
    1.  Le reverse proxy Keycloak (`rp-k`) agit comme une passerelle vers une autre instance Keycloak.
    2.  Il reçoit les requêtes et les relaie vers le serveur Keycloak spécifié.

- **Fichiers importants :**
    - `rp-k/Dockerfile`: Instructions pour construire l'image Docker du reverse proxy Keycloak.
    - `rp-k/conf/httpd.conf`: Fichier de configuration Apache pour le reverse proxy.
    - `rp-k/conf/httpd-vhosts.conf`: Fichier de configuration Apache pour les virtual hosts.

### 5. Reverse Proxies

#### Reverse Proxy (Application C) (`reverse-proxy/`)

- **Fonctionnement :**
    1. L'utilisateur accède au reverse proxy pour l'application C (`http://auth.test:8085`).
    2. Le reverse proxy vérifie si l'utilisateur est authentifié auprès de Keycloak.
    3. Si l'utilisateur n'est pas authentifié, le reverse proxy redirige l'utilisateur vers Keycloak pour l'authentification.
    4. Keycloak authentifie l'utilisateur (nom d'utilisateur et mot de passe).
    5. Keycloak redirige l'utilisateur vers le reverse proxy.
    6. Le reverse proxy extrait les informations de l'utilisateur (nom, rôles) du jeton d'accès fourni par Keycloak.
    7. Le reverse proxy transmet les informations de l'utilisateur à l'application C via les en-têtes HTTP (`X-User-Name`, `X-User-Roles`) (reverse-proxy/oidc.conf:24-25).

- **Fichiers importants :**
    - `reverse-proxy/Dockerfile`: Instructions pour construire l'image Docker du reverse proxy.
    - `reverse-proxy/proxy.conf`: Configuration Apache pour le reverse proxy.
    - `reverse-proxy/oidc.conf` (reverse-proxy/oidc.conf:1-30): Configuration OIDC pour le reverse proxy.

#### Reverse Proxy (Application D) (`rp-d/`)
Même architecture que pour celui de l'application C.

#### Reverse Proxy (Application E) (`reverse-proxy-user/`)

- **Fonctionnement :**
    1. L'utilisateur accède à l'application E via le reverse proxy (`http://user/app`).
    2. Si l'utilisateur n'est pas connecté, l'application E affiche un lien vers la page de connexion (`+/login`).
    3. Lorsque l'utilisateur clique sur le lien de connexion, il est redirigé vers Keycloak en restant sur le reverse proxy pour l'authentification.

- **Fichiers importants :**
    - `reverse-proxy-user/Dockerfile`: Instructions pour construire l'image Docker du reverse proxy.
    - `reverse-proxy-user/conf/httpd.conf`: Configuration Apache pour le reverse proxy.
    - `reverse-proxy-user/conf/httpd-vhosts.conf`: Virtual host configuration pour le reverse proxy.

#### Reverse Proxy (Administration Keycloak) (`reverse-proxy-admin/`)

- **Fonctionnement :**
    1. L'utilisateur accède à l'interface d'administration de Keycloak via le reverse proxy (`http://admin`).
    2. Le reverse proxy relaie les requêtes vers le serveur Keycloak.

- **Fichiers importants :**
    - `reverse-proxy-admin/Dockerfile`: Instructions pour construire l'image Docker du reverse proxy.
    - `reverse-proxy-admin/conf/httpd.conf`: Configuration Apache pour le reverse proxy.
    - `reverse-proxy-admin/conf/httpd-vhosts.conf`: Virtual host configuration pour le reverse proxy.

### 6. Proxy DNS (`dns-proxy/`)

- Fournit une résolution de noms de domaine personnalisée pour les services à l'intérieur du réseau Docker.
- Utilise le fichier `dnsmasq.conf` pour configurer les mappings de noms de domaine vers les adresses IP des conteneurs.

## Structure du Projet

- **`docker-compose.yml`:** Définit les services Docker et les configurations réseau.
- **`application-a/`:** Code source de l'application A.
    - **`Dockerfile`:** Instructions pour construire l'image Docker de l'application A.
    - **`app.py`:** Le code Python principal de l'application A utilisant Flask et Authlib.
    - **`requirements.txt`:** Les dépendances Python de l'application A.
    - **`templates/`:** Templates HTML pour l'application A.
- **`application-b/`:** Code source de l'application B.
    - **`Dockerfile`:** Instructions pour construire l'image Docker de l'application B.
    - **`app.py`:** Le code Python principal de l'application B utilisant Flask et Authlib.
    - **`requirements.txt`:** Les dépendances Python de l'application B.
- **`application-c/`:** Code source de l'application C.
    - **`Dockerfile`:** Instructions pour construire l'image Docker de l'application C.
    - **`app.py`:** Le code Python principal de l'application C utilisant Flask.
    - **`templates/`:** Templates HTML pour l'application C.
    - **`requirements.txt`:** Les dépendances Python de l'application C.
- **`application-d/`:** Code source de l'application D.
    - **`Dockerfile`:** Instructions pour construire l'image Docker de l'application D.
    - **`app.py`:** Le code Python principal de l'application D utilisant Flask et Authlib.
    - **`requirements.txt`:** Les dépendances Python de l'application D.
    - **`templates/`:** Templates HTML pour l'application D.
- **`application-e/`:** Code source de l'application E.
    - **`Dockerfile`:** Instructions pour construire l'image Docker de l'application E.
    - **`app.py`:** Le code Python principal de l'application E utilisant Flask.
    - **`templates/`:** Templates HTML pour l'application E.
    - **`requirements.txt`:** Les dépendances Python de l'application E.
- **`reverse-proxy/`:** Code source du reverse proxy pour l'application C.
    - **`Dockerfile`:** Instructions pour construire l'image Docker du reverse proxy.
    - **`proxy.conf`:** Fichier de configuration Apache pour le proxy.
    - **`oidc.conf`:** Configuration Apache pour l'authentification OpenID Connect avec Keycloak.
    - **`secret.conf`:** Contient le secret client utilisé par le reverse proxy.
- **`reverse-proxy-user/`:** Code source du reverse proxy pour l'application E.
    - **`Dockerfile`:** Instructions pour construire l'image Docker du reverse proxy.
    - **`conf/httpd.conf`:** Fichier de configuration Apache pour le proxy.
    - **`conf/httpd-vhosts.conf`:** Fichier de configuration Apache pour les virtual hosts.
- **`reverse-proxy-admin/`:** Code source du reverse proxy pour l'administration de Keycloak.
    - **`Dockerfile`:** Instructions pour construire l'image Docker du reverse proxy.
    - **`conf/httpd.conf`:** Fichier de configuration Apache pour le proxy.
    - **`conf/httpd-vhosts.conf`:** Fichier de configuration Apache pour les virtual hosts.
- **`rp-d/`:** Code source du reverse proxy pour l'application D.
    - **`Dockerfile`:** Instructions pour construire l'image Docker du reverse proxy.
    - **`proxy.conf`:** Fichier de configuration Apache pour le proxy.
    - **`oidc.conf`:** Configuration Apache pour l'authentification OpenID Connect avec Keycloak.
- **`rp-k/`:** Code source du reverse proxy pour Keycloak.
    - **`Dockerfile`:** Instructions pour construire l'image Docker du reverse proxy.
    - **`conf/httpd.conf`:** Fichier de configuration Apache pour le proxy.
    - **`conf/httpd-vhosts.conf`:** Fichier de configuration Apache pour les virtual hosts.
- **`keycloak/`:** Contient la configuration du realm pour Keycloak.
    - **`realm.json`:** Configure le realm, les utilisateurs, les rôles et les clients dans Keycloak.
- **`idp/`:** Contient la configuration du realm pour Keycloak Identity Provider.
    - **`realm.json`:** Configure le realm, les utilisateurs, les rôles et les clients dans Keycloak.
- **`dnsmasq.conf`:** Fichier de configuration pour le proxy DNS.
- **`.git/`:** Fichiers de configuration du dépôt Git.
