#!/bin/sh

echo "Criando as migrations"

python3 manage.py makemigrations

echo "Aplicando as migrations"

python3 manage.py migrate

echo "Iniciando a aplicação"

python3 manage.py runserver 0.0.0.0:8080 --noreload