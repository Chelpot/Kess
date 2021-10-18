release: python mysite/manage.py makemigrations
release: python mysite/manage.py migrate
web: gunicorn mysite.wsgi:application --log-file -