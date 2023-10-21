Initialize Project and then give required names
```
cookiecutter https://github.com/CalledSidd/GHL-Cookiecutter 
```
Generate a secret key: <a href="https://djecrety.ir/">Secret Key Generator</a>

change env.text filename to .env, then add the generated secret key
runserver to check if everything is working
```
python manage.py runserver
```
if working migrate
```
python manage.py makemigrations
python manage.py migrate
```
<h1>GoHighLevel Setup</h1>
<p>When using GHL 2.0, you will need the CLIENT ID, the CLIENT SECRET, add them to the .env file</p>
<h1>Make the templates functional</h1>
<p>On the base url styles will not be loaded to load the styles</p>
add these lines on base.html

```
    {% block content %}
    {% endblock content %}
```
and these lines to the get.html

```
{% extends "base.html" %}
{% block content %}
    <!--HTML CONTENT-->
{% endblock content %}
```