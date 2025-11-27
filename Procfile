web: gunicorn manifest_system.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput
