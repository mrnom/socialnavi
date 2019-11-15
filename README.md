## SocialNavi
Basic social network API with JWT authentication based on Django REST Framework.

### Third party API calls
Create `local_settings.py` next to `settings.py`.

#### Hunter Email Verifier

Set `HUNTER_API_KEY` (https://hunter.io/api_keys) in `local_settings.py`
if you need to verify user email on register.

#### Clearbit Enrichment
Set `CLEARBIT_API_KEY` (https://dashboard.clearbit.com/api) in `local_settings.py` 
to enrich user account with additional data on register.

### Setup
```
pipenv --three
pipenv install --dev
python manage.py migrate
```

#### Run tests
```
python manage.py test
```

### Run server
```
python manage.py runserver
```
#### OpenAPI specification
Visit `http://localhost:8000/swagger/` to check out available endpoints.

> Comment out `HUNTER_API_KEY` in `local_settings.py` if you are using 
fake email.

1. Try out `POST /users/` with email and password to create a new user.

2. `POST /api/token/` with the same credentials to obtain an auth token.

3. Copy `access` token from a response body.

4. Authorize with `Bearer <your_access_token>` to unlock the rest of the endpoints.
