## SocialNavi
Basic social network API with JWT authentication based on Django REST Framework.

Create `local_settings.py` next to `settings.py` 
and make sure you've set `HUNTER_API_KEY` (https://hunter.io/api_keys)
if you need to verify user email on register.

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
