# Keycloak Multi-Application Setup

This project demonstrates a multi-application setup using Keycloak for authentication and authorization. It includes three applications (A, B, and C), a reverse proxy, and a DNS proxy, all orchestrated with Docker Compose.

## Overview

- **Keycloak:** The identity and access management server.
- **Application A & B:** Python-based Flask applications that require user authentication via Keycloak. Application B requires the admin role.
- **Application C:** A Python-based Flask application that displays user information extracted from headers by the reverse proxy.
- **Reverse Proxy:** An Apache server acting as a gateway, authenticating requests via Keycloak and passing user information in headers to Application C.
- **DNS Proxy:** A DNS server for custom domain resolution inside the Docker network.

## Features

- **Centralized Authentication:** Keycloak manages user authentication for Applications A and B.
- **Role-Based Access Control:** Application B is only accessible by users with the "admin" role.
- **Single Sign-On (SSO):** Once authenticated, users can access the applications without re-authenticating.
- **Reverse Proxy Authentication:** The reverse proxy handles authentication before forwarding requests to Application C, injecting user information in headers.
- **Custom DNS:** The DNS proxy allows accessing services within the Docker network using custom domain names like `auth.test`.
- **Configurable Home Text:** Application A allows admin users to change the displayed welcome text.

## Installation

1. **Clone the project:**

   ```shell
   git clone https://github.com/randomKara/keycloak_set_test
   ```

2. **Navigate to the project directory:**

   ```shell
   cd keycloak_set_test/
   ```

3. **Launch the project using Docker Compose:**

   ```shell
   docker-compose up --build
   ```

4. **DNS Configuration:** Add the project subnet to your system's DNS configuration. This is required so the reverse proxy works correctly.

   - **Non-Permanent:** Execute the following command each time you start your PC.

      ```shell
      sudo sed -i '2i nameserver 172.28.0.1' /etc/resolv.conf
      ```
 

## Usage

1. **Access Keycloak:**
   - Open your web browser and navigate to `http://localhost:8080`.
   - Log in with the default admin credentials:
     - **Username:** `admin`
     - **Password:** `admin`

2. **Access Applications:**
   - **Application A:** Navigate to `http://localhost:5000`. 
   - **Application B:** Navigate to `http://localhost:5001`.
   - **Application C:** Navigate to `http://auth.test:8085`. The authentication is handle by the reverse proxy before being redirected to Application C. You can navigate to `http://localhost:5002` to go directly to access Application C, but the information fields will be empty because there is nothing in the header. 

3. **Log in via Keycloak:**
   - When accessing either Application A or B, you will be redirected to Keycloak for login.
   - Log in using the following credentials:
     - **User:**
       - **Username:** `user`
       - **Password:** `user`
     - **Admin:**
       - **Username:** `admin`
       - **Password:** `admin`
   - Application B requires the "admin" role; so login with the admin user to access its home page.

4. **Application Functionalities:**
   - **Application A:** Displays a welcome message. If you log in with the admin user, a form is displayed which allows you to modify the welcome text.
   - **Application B:** Displays a specific welcome message if the user has the admin role.
   - **Application C:** Displays the user's name and roles extracted from the headers by the reverse proxy.

## Project Structure

- **`docker-compose.yml`:** Defines the Docker services and network configurations.
- **`.env`:** Environment variables for the project.
- **`application-a/`:** Source code for Application A.
    - **`Dockerfile`:** Instructions to build Application A's Docker image.
    - **`app.py`:** The main Python code for Application A using Flask and Authlib.
    - **`requirements.txt`:** Application A's Python dependencies.
    - **`templates/`:** HTML templates for Application A.
- **`application-b/`:** Source code for Application B.
    - **`Dockerfile`:** Instructions to build Application B's Docker image.
    - **`app.py`:** The main Python code for Application B using Flask and Authlib.
    - **`requirements.txt`:** Application B's Python dependencies.
- **`application-c/`:** Source code for Application C.
    - **`Dockerfile`:** Instructions to build Application C's Docker image.
    - **`app.py`:** The main Python code for Application C using Flask.
     - **`templates/`:** HTML templates for Application C.
    - **`requirements.txt`:** Application C's Python dependencies.
- **`reverse-proxy/`:** Source code for the reverse proxy.
    - **`Dockerfile`:** Instructions to build the reverse proxy's Docker image.
    - **`proxy.conf`:** Apache configuration file for the proxy.
    - **`oidc.conf`:** Apache configuration for OpenID Connect authentication with Keycloak.
    - **`secret.conf`:** Contains the client secret used by the reverse proxy.
- **`keycloak/`:** Contains the realm configuration for Keycloak.
  - **`realm.json`:** Configures the realm, users, roles, and clients in Keycloak.
- **`dnsmasq.conf`:** Configuration file for the DNS proxy.
- **`.git/`:** Git repository configuration files.

## Explanation of the Code
A more detailed code explanation is available in the ISSUES.md file in the github repository.
