# Utilise une image officielle Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt (à créer)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY ./app ./app

# Exposer le port 8000 (FastAPI par défaut)
EXPOSE 8000

# Commande pour lancer FastAPI avec uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
