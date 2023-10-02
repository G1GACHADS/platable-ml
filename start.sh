set -ex

source venv/bin/activate

nohup gunicorn wsgi:app --name platable-ml -b 0.0.0.0:80 --timeout 120 >log.txt 2>&1 &
