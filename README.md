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
