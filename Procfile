web: gunicorn authors.wsgi --log-file -
release: python manage.py makemigrations authentication; python manage.py makemigrations profiles; python manage.py makemigrations articles; python manage.py migrate;
