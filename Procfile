release: python mysite/manage.py migrate
web: gunicorn --chdir mysite mysite.wsgi --log-file -