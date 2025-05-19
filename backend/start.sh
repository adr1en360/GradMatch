nohup langflow --host 0.0.0.0 --port 7860 --file langflow/AI_flow.json > ../langflow.log 2>&1 &
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn GradMatch.wsgi:application --bind 0.0.0.0:$PORT

