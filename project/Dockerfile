# Utilisation de l'image officielle Python
FROM python:3.11-slim

# Définit les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste des fichiers du projet
COPY . /app/

# Collecter les fichiers statiques (optionnel, utile pour la production)
RUN python manage.py collectstatic --noinput

# Exposer le port 8000 (ou autre si tu en utilises un autre)
EXPOSE 8000

# Commande de démarrage de l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
