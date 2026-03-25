#!/bin/sh

set -e

until python manage.py migrate; do
	echo "Aguardando banco de dados..."
	sleep 2
done

python manage.py runserver 0.0.0.0:8000
