set -ex

source venv/bin/activate

gunicorn wsgi:app \
    --name platable-ml \
    -b 0.0.0.0:80 \
    --timeout 120
