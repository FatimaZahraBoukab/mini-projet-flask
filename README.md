🔐 Gestionnaire de Profil Flask
Une application web Flask complète pour la gestion des profils utilisateurs avec authentification sécurisée.
✨ Fonctionnalités

📝 Inscription : Création de compte utilisateur
🔑 Connexion/Déconnexion : Authentification sécurisée
👤 Gestion du profil : Modification des informations personnelles
🔒 Changement de mot de passe : Sécurité renforcée
📸 Photo de profil : Upload et modification d'avatar
📊 Historique des connexions : Suivi des dernières sessions
🚪 Déconnexion sécurisée : Gestion propre des sessions

🛠️ Technologies utilisées

Backend : Flask (Python)
Base de données : SQLite/PostgreSQL
Frontend : HTML, CSS, JavaScript
Authentification : Flask-Login
Upload de fichiers : Flask-WTF
Hashage des mots de passe : Werkzeug

📦 Installation

Cloner le repository
bashgit clone https://github.com/votre-username/flask-profile-manager.git
cd flask-profile-manager

Créer un environnement virtuel
bashpython -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

Installer les dépendances
bashpip install -r requirements.txt

Configuration
bashexport FLASK_APP=app.py
export FLASK_ENV=development

Initialiser la base de données
bashflask db init
flask db migrate
flask db upgrade


🚀 Utilisation

Lancer l'application
bashpython app.py

Accéder à l'application

Ouvrez votre navigateur
Allez sur http://localhost:5000


Première utilisation

Créez un compte via la page d'inscription
Connectez-vous avec vos identifiants
Explorez les fonctionnalités du profil
