# Projet 11


### Principe et configuration nécessaire :
Il s'agit de reprendre en cours un projet en construction et de configurer les tests.
Le projet a été créé avec Flask et plusieurs bugs ont été détectés et doivent être corrigés.
Ce projet nécessite d'installer python.

## Installation
### Fichiers du site
Sur le terminal se placer sur un dossier cible.

Puis suivre les étapes suivantes :
1. Cloner le dépôt ici présent en tapant: `$ git clone https://github.com/S0Imyr/Projet-11.git`
2. Accéder au dossier ainsi créé avec la commande : `$ cd Projet-11`
3. Créer un environnement virtuel pour le projet avec 
    - `$ python -m venv env` sous windows 
    - ou `$ python3 -m venv env` sous MacOS ou Linux.
4. Activez l'environnement virtuel avec 
    - `$ source env/Scripts/activate` sous windows 
    - ou `$ source env/bin/activate` sous MacOS ou Linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`


### Lancement du serveur
Dans le terminal tapper :

6. Définir le fichier python qui lance le serveur avec : `export FLASK_APP=server.py`
7. Démarrer le serveur avec `$ flask run`

Lorsque le serveur fonctionne, après l'étape 7 de la procédure, le site est accessible avec l'url : [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Arrêter le serveur

Pour arrêter le serveur aller dans le terminal où il a été lancé, puis appuyer sur les touches Ctrl+C.

## Tests et couverture

Pour lancer les test, se placer dans le terminal dans le dossier : projet-11/projet11.

Puis tapper : `$ pytest`.

Pour obtenir la couverture utiliser les commandes :
 - `$ coverage run -m pytest`
 - `$ coverage report`

## Performances

Pour évaluer les performances de l'application, on peut utiliser locust.
On débutera par lancer l'application sur un terminal puis en laissant l'application tourner :

 - taper dans un second terminal : `$ locust `
 - puis se rendre à l'url [http://localhost:8089/](http://localhost:8089/)

 Il faut ensuite renseigner plusieurs champs, on pourra par exemple tester avec :
 - Number of total users to simulate : 100
 - Spawn rate : 10
 - Host : http://127.0.0.1:5000