release: python mysite/manage.py migrate
release: python mysite/manage.py makemigrations
web: gunicorn mysite/mysite/wsgi.py:application --log-file -