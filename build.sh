set -o errexit

pip3 install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py scrape_hotels
DJANGO_SUPERUSER_PASSWORD=Damin@321 python3 manage.py createsuperuser --noinput --username=admin1 --email=admin1@admin1.com