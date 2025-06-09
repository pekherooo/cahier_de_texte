FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libcairo2 \
    libffi-dev \
    libjpeg-dev \
    libgdk-pixbuf2.0-0 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# On définit le dossier de travail correctement (à adapter selon ton arborescence réelle)
WORKDIR /cahier_de_texte_base

# On copie tout ton projet dans /app
COPY . .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Et là attention au point d’entrée WSGI
# Vérifie bien où se trouve ton wsgi.py
# Exemple si ton wsgi.py est à la racine : /app/wsgi.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
