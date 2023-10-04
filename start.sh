set -ex

source venv/bin/activate

sudo nohup $(which gunicorn) wsgi:app \
    --name platable-ml -b 0.0.0.0:80 --timeout 120 \
    -w 4 --threads 4 \
    >log.txt 2>&1 &
