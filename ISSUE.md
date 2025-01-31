# ISSUE.md

This document summarizes the issues encountered and resolved during the development of a multi-application setup using Keycloak for authentication and authorization. The focus is on the final working solutions implemented.

## 1. Initial Setup and Keycloak Configuration

### Issue: Keycloak Not Starting Correctly
*   **File:** `docker-compose.yml`
*   **Functionality:** Keycloak container startup.
*   **Issue:** The Keycloak container was not starting correctly, leading to a failed deployment. The logs showed `Unknown option: \u00270.0.0.0\u0027` indicating an issue with the command used to start keycloak.
*   **Solution:** The `command` for the Keycloak service was modified to use the correct syntax for starting Keycloak in development mode: `command: ["start-dev", "--hostname-strict\u003dfalse"]`.

### Issue: Keycloak Realm Not Imported
*   **File:** `docker-compose.yml`
*   **Functionality:** Keycloak realm import at startup.
*   **Issue:** The Keycloak realm was not being imported during the container startup, leading to a 404 error when applications tried to access the metadata.
*   **Solution:** The `command` for the Keycloak service was updated to include the `--import-realm` flag, ensuring the realm is imported at startup: `command: ["start-dev", "--import-realm"]`.

### Issue: Applications Starting Before Keycloak
*   **File:** `docker-compose.yml`
*   **Functionality:** Application startup dependency on Keycloak.
*   **Issue:** The applications (`application-a` and `application-b`) were starting before Keycloak was fully initialized, leading to connection errors.
*   **Solution:** A `healthcheck` was added to the Keycloak service, and the `depends_on` condition in the application services was updated to `service_healthy`. This ensures that the applications start only after Keycloak is fully operational:
    ```yaml
    depends_on:
        keycloak:
          condition: service_healthy
    ```

## 2. Application Configuration

### Issue: Missing `requests` Module
*   **File:** `application-a/requirements.txt`, `application-b/requirements.txt`
*   **Functionality:** Dependency management for applications A and B.
*   **Issue:** The applications were failing with `ModuleNotFoundError: No module named \u0027requests\u0027` because the `requests` library was missing from the `requirements.txt` files.
*   **Solution:** The `requests` library was added to the `requirements.txt` files of both applications.

### Issue: `OIDC_REQUIRE_VERIFIED_EMAIL` Configuration Error
*   **File:** `application-a/app.py`, `application-b/app.py`
*   **Functionality:** Configuration of `flask-oidc` for authentication.
*   **Issue:** The applications were failing with `ValueError: The \u0027OIDC_REQUIRE_VERIFIED_EMAIL\u0027 configuration value is no longer enforced.` because this option is deprecated in recent version of `flask-oidc`.
*   **Solution:** The `OIDC_REQUIRE_VERIFIED_EMAIL` configuration line was removed from the `app.py` files.

## 3. Reverse Proxy Configuration

### Issue: `OIDCRedirectURI` Mismatch
*   **File:** `reverse-proxy/oidc.conf`, `keycloak/realm.json`
*   **Functionality:** Configuration of `mod_auth_openidc` for authentication.
*   **Issue:** The reverse proxy was encountering an `oidc_request_check_cookie_domain` error because the `OIDCRedirectURI` in the `oidc.conf` file did not match the URL used to access the application.
*   **Solution:** The `OIDCRedirectURI` in `oidc.conf` was changed to `http://auth.test:8085/oauth2callback` to match the URL used to access the application. The `redirectUris` in `keycloak/realm.json` was also updated to include `http://auth.test:8085/oauth2callback`.

### Issue:  `OIDCRemoteUserClaim` Error
*   **File:** `reverse-proxy/oidc.conf`
*   **Functionality:** Configuration of `mod_auth_openidc` for authentication.
*   **Issue:** The reverse proxy was failing because the `OIDCRemoteUserClaim` was set to `principal`, which is not a standard claim in the JWT token.
*   **Solution:** The `OIDCRemoteUserClaim` was changed to `name`, which is a standard claim, and the `RequestHeader` was updated to use the correct variable `%{OIDC_CLAIM_name}e`.

### Issue:  `realm_access` Not Included in `id_token`
*   **File:** `keycloak/realm.json`
*   **Functionality:** Keycloak realm configuration.
*   **Issue:** The `realm_access` claim was not included in the `id_token` by default.
*   **Solution:** A protocol mapper was added to the client configurations in `realm.json` to include the `realm_access` claim in the `id_token`. Forcing a protocal mapper attribute means that none will be generated automatically. A complete mapping is therefore required. Tip: export the realm (without the users) and put it in the `realm.json` with the desired modifications.


## 4. DNS Configuration


### 1. Initial DNS Resolution Issue with Keycloak

*   **File:** `docker-compose.yml`, `application-a/app.py`, `application-b/app.py`
*   **Functionality:** Initial setup of Keycloak and application connectivity.
*   **Issue:** The applications (A and B) were unable to resolve the hostname `keycloak` when trying to access the Keycloak server's metadata endpoint. This resulted in a `requests.exceptions.ConnectionError` or a `404 Client Error` because the applications were using the `keycloak` hostname, which is only resolvable within the Docker network, and not from the host machine.
*   **Solution:** The `KEYCLOAK_URL` variable in the `docker-compose.yml` was initially changed to `http://localhost:8080` to allow the applications to connect to Keycloak. However, this caused a new issue where the applications were trying to connect to `localhost` *from inside the container*, which does not refer to the host machine. The solution was to revert this change and use `http://keycloak:8080` in the `docker-compose.yml` and to add a DNS server.

