release: python mysite/manage.py migrate
release: python mysite/manage.py makemigrations
web: gunicorn mysite.wsgi --log-file -