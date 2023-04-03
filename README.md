# Projet statistiques

### Objectifs du projet

A la suite de l'upload du fichier csv fournis sur classroom, être capable d'effectuer au moins 3 tests statistiques differents et de les sauvegarder dans votre base de donnée

### Install

Créer un environnement virtuel et installer vos dependances

```
virtualenv .venv
.venv\\Scripts\\activate # windows
```
Installer les dependances
```
pip install -r requirements.txt
```

##### Créer votre base de donnée
Créer une base de donnée PGSQL et entrer les informations dans un fichier .env a la racine du projet
```
DATABASE_NAME=<your_database_name>
DATABASE_PWD=<your_database_password>
DATABASE_USER=<your_database_user>
```

##### Executer vos migrations django

Pour créer les tables dans la base de donnée, il faut executer vos migrations.

Créer vos migrations
```
py manage.py makemigrations
```

Effectuer les migrations

```
py manage.py migrate
```

##### Créer votre super utilisateur pour acceder à l'administration

```
py manage.py createsuperuser
```

### Run

```
py manage.py runserver
```

### Help

bastien.angeloz.int@groupe-gema.com

### Licence

MIT