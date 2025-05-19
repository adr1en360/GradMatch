nohup langflow &
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn GradMatch.wsgi:application --bind 0.0.0.0:$PORT