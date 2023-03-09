# Archivo Bash para instalar la apo en linux
#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
# Instalacion de las dependencias del sistema en el hosting
# pip install -r  requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate