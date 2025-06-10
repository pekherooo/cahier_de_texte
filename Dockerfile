FROM python:3.10-slim

# Installer wkhtmltopdf et dépendances
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    fontconfig \
    libxrender1 \
    libxext6 \
    libx11-6 \
    && wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltopdf_0.12.6-1.buster_amd64.deb \
    && apt install -y ./wkhtmltopdf_0.12.6-1.buster_amd64.deb \
    && rm wkhtmltopdf_0.12.6-1.buster_amd64.deb

WORKDIR /cahier_de_texte_base

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
