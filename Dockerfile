FROM python:3.10-slim

# Installer juste les dépendances système de base (optionnel)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libjpeg-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cahier_de_texte_base

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
