[![CI](https://github.com/SebGoliot/oc_p8-purbeurre/actions/workflows/main.yml/badge.svg)](https://github.com/SebGoliot/oc_p8-purbeurre/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/SebGoliot/oc_p8-purbeurre/branch/main/graph/badge.svg?token=I6ZNSERW7R)](https://codecov.io/gh/SebGoliot/oc_p8-purbeurre)

# OC P8 - PurBeurre
## 1. Présentation
PurBeurre est une plateforme web à destination des clients de la startup du même nom.  
Ce site permet à quiconque le souhaite de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que le gras c’est la vie).

Le projet déployé sur Heroku est [disponible ici](https://nutella-pur-beurre.herokuapp.com)

## 2. Fonctionnalités
Plusieurs fonctionnalités sont nécessaires pour la réalisation de ce projet:
- Affichage du champ de recherche dès la page d’accueil
- La recherche ne doit pas s’effectuer en AJAX
- Interface responsive
- Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de passe pour le moment.

## 3. Pré-requis
Python >= 3.9 (
    Utilisation de `|=` sur des `dict`: 
    [PEP 584](https://www.python.org/dev/peps/pep-0584/))  
Un serveur de base de données Postgres  
- Vous pouvez utiliser le fichier docker-compose.yml fourni pour lancer une instance de Postgres

## 4. Utilisation

### Debug
Pour lancer l'application en debug, il suffit de:
- Créer un environnement virtuel: `python -m venv venv`
- Activer cet environnement virtuel:
    - Windows : `.\venv\Scripts\Activate.ps1`
    - Linux / Mac : `source venv/bin/activate`
- Installer les dépendances: `pip install -r requirements.txt`
    - Si vous souhaitez lancer les tests, vous devrez aussi installer les dépendances de test:  
      - `pip install -r test_requirements.txt`
- Créer une variable d'environnement `SECRET_KEY` avec la clé secrète de Django
- Lancer le serveur de base de données Postgres
- Créer les migrations: `python manage.py makemigrations accounts nutella`
- Appliquer les migrations: `python manage.py migrate`
- Ajouter des catégories en base de donnée:
    - `python manage.py add_category` avec le nom de la catégorie
    - lorsque toutes les catégories nécessaires auront été ajoutées, mettez à jour la base de données avec:
        - `python manage.py update_db`
- Lancer le serveur de test: `python manage.py runserver`


### Production
Le déploiement en production s'est déroulé de la façon suivante:
- Création d'une app Heroku
- Ajout des variables d'environnement nécessaires (Config Vars):
    - `SECRET_KEY` avec la clé secrète de Django
    - `ENV` avec `PRODUCTION`
- Dans Deploy:
    - Activation de `Github` comme méthode de déploiement
    - Connexion au dépôt du projet
    - Activation du déploiement automatique, avec l'option `Wait for CI to pass before deploy`
- Une fois le projet déployé, entrée dans la console:
    - `python manage.py makemigrations accounts nutella`
    - `python manage.py migrate`
    - `python manage.py import_products 1000`
