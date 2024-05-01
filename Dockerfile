# Utilise l'image de base Python
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances dans le conteneur
COPY ./app/requirements.txt /app/requirements.txt

# Installe les dépendances
RUN pip install -r requirements.txt

# Copie le code de l'application dans le conteneur
COPY ./app /app

# Définit la variable d'environnement REPLICATE_API_TOKEN
ENV REPLICATE_API_TOKEN=XXX

# Expose le port 80 pour les requêtes HTTP
EXPOSE 80

# Démarre l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]