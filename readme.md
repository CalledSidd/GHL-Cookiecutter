Initialize Project and then give required names
```
cookiecutter https://github.com/CalledSidd/GHL-Cookiecutter 

Generate a secret key: <a href="https://djecrety.ir/">Secret Key Generator</a>

change env.text filename to .env, then add the generated secret key

```
runserver to check if everything is working
```
python manage.py runserver
```
if working migrate
```
python manage.py makemigrations
python manage.py migrate
```