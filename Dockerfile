# Image de base Debian pour pouvoir installer les dépendances de WeasyPrint
FROM python:3.13-slim

# Install packages système nécessaires à WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libcairo2 \
    libffi-dev \
    libjpeg-dev \
    libgdk-pixbuf2.0-0 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier ton code
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Point d'entrée WSGI
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
