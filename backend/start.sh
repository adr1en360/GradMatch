nohup langflow &

gunicorn GradMatch.wsgi:application --bind 0.0.0.0:$PORT