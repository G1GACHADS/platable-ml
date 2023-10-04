set -ex

gunicorn wsgi:app \
    --name platable-ml -b 127.0.0.1:5000 --timeout 120 \
    -w 4 --threads 4
