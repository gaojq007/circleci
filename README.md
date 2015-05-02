Pour ma mise en oeuvre, j'ai suivi le site : 
https://realpython.com/blog/python/docker-in-action-fitter-happier-more-productive/

DOCKER IN ACTION : Integration Continue avec CircleCI 

Nous allons installé notre environnement local, en buildant une image à partir d'un Dockerfile puis créer une instance de l'image à partir du conteneur . Nous attacherons le tout avec Docker Compose pour builder et connecter différents conteneurs à la fois pour l'application et le processus Flask Redis .

PREREQUIS

DOCKER HUB
Prérequis : 
	- avoir un compte sur docker hub (https://registry.hub.docker.com/u/<user>)
	- ajouter un repository : <user>/ci-project 

CONNECTION à DOCKER HUB
Connection à Docker Hub, par ligne de commande :
user@server1:~$ sudo docker login
Importer notre image du docker hub
	docker pull <user>/ci-project

Installation d'une VM ubuntu 14.04 sur virtualbox
Configurer ssh puis activer
	$ sudo apt-get install ssh
$ sudo service ssh start
Mettre à jour les paquets
$ sudo apt-get update
Installer Docker (version la plus récente)
	$ wget -qO- https://get.docker.com/ | sh
Vérifier que Docker est bien installé
	$ sudo docker run hello-world
	$ docker images
Ajouter un group "docker" et y ajouter votre user
	$ sudo usermod -aG docker <user>
Rebooter puis vérifier que vous pouvez utiliser Docker sans "sudo"
	$ docker run hello-world
Récupérer les fichiers du projet
git clone https://github.com/realpython/fitter-happier-docker.git
Renommer le répertoire 
	mv fitter-happier-docker ci-project
	cd ci-project

DOCKER
======
DOCKERFILE

Le répertoire où sera le Dockerfile a été ajouté :
	/home/user/ci-project/web
#  Dockerfile :
	$ nano /home/user/ci-project/web/Dockerfile
# start with a base image
FROM ubuntu:14.10

# install dependencies
RUN apt-get -y update
RUN apt-get install -y python python-dev python-pip python-psycopg2
RUN apt-get install -y nginx supervisor

# add requirements.txt and install
ADD requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

# set working diretory
WORKDIR /code 
# fichier "requirements.txt"
		docker-py==0.5.3
docopt==0.6.2
Flask==0.10.1
Flask-Testing==0.4.2
itsdangerous==0.24
Jinja2==2.7.3
MarkupSafe==0.23
nose==1.3.4
PyYAML==3.11
redis==2.10.3
requests==2.2.1
six==1.9.0
texttable==0.8.2
websocket-client==0.11.0
Werkzeug==0.10.1

DOCKER COMPOSE
L’objectif de “docker-compose” est de permettre d’exécuter et de mettre en relation les différentes images dont notre application a besoin en une seule commande. Un fichier docker-compose.yml doit être créé. Chaque container doit y être décrit : image, commande de lancement, volumes, ports…

Installer Docker Compose
$ curl -L https://github.com/docker/compose/releases/download/1.2.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
$ chmod +x /usr/local/bin/docker-compose
Tester l'installation de Compose
	$ docker-compose --version
	$ sudo nano docker-compose.yml
 web:
    build: web
    volumes:
        - web:/code
    ports:
        - "80:5000"
    links:
        - redis
    command: python app.py
redis:
    image: redis:2.8.19
    ports:
        - "6379:6379"

Ici, nous ajoutons les services qui composent notre pile :
1. web : tout d'abord, nous buildons l'image à partir du répertoire "web" et puis on monte ce répertoire dans le répertoire "code" dans le conteneur Docker . L'application Flask est lancé par la commande python app.py. Cela expose le port 5000 sur le conteneur, qui est transmise au port 80 de l'environnement hôte .
2. redis : ensuite, le service Redis est buildé à partir de l'image "Redis" du Docker Hub. Port 6379 est exposé et transmis.

Noter que le Dockerfile et dans le répertoire "web". Ce fichier est utilisé pour builder notre image, à partir d'une base ubuntu, les dépendances requises sont installées et l'appli buildée

Build et exécution
Avec une simple commande on peut builder une image et lancer le conteneur :
$ docker-compose up

Erreur " client and server don't have same version (client : 1.15, server: 1.12)" ==> docker upgrade
$ wget -qO- https://get.docker.io/gpg | sudo apt-key add -
$ sudo sh -c "echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install lxc-docker  

# récupérer l'adresse IP docker : ifconfig/docker0
IP docker : 172.17.42.1
 

Pour se connecter à partir du navigateur de la machine hôte, dans virtualbox, pour notre VM, faire une redirection de port : 5000 à 80.==>  http://localhost:5000/
 
	$ docker ps
	$ docker-compose ps

Arrêter docker compose
	$ docker-compose stop
Créer une image
	$ cd /web	# aller dans le répertoire qui contient le Dockerfile (/home/user/ci-project/web)
	$ docker build -t="<user>/ci-project" .
Vérifier que l'image a été buildée 
	$ docker images
 
Déposer l'image dans docker hub
	$ docker push <user>/ci-project

Nous avons installer notre environnement local, en détaillant le processus de base de la construction d' une image d'un Dockerfile puis créer une instance de l'image (un conteneur) . Nous avons attaché le tout avec Docker Compose pour builder et connecter différents conteneurs à la fois pour l'application et le processus Flask Redis. Maintenant nous allons mettre en oeuvre l'intégration continue avec CircleCI.

TUTO GIT
========
http://git-scm.com/book/fr/v1/D%C3%A9marrage-rapide-Installation-de-Git

1°) Installer git sur son serveur ubuntu

$ apt-get update
$ apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev
$ apt-get install git
$ wget http://pkgs.fedoraproject.org/repo/pkgs/git/git-2.3.6.tar.gz/c29ac45bde67545b7e7941903000f6d3/git-2.3.6.tar.gz
$ tar -zxf git-2.3.6.tar.gz
$ cd git-2.3.6
$ make prefix=/usr/local all
$ sudo make prefix=/usr/local install
# Nom d’utilisateur : dire à git votre nom, pour qu'il étiquette les commits 
$ git config --global user.name "<user>"
# E-mail : Git sauvegarde l'adresse e-mail à l’intérieur des commits produits. 
# L’adresse e-mail est utilisée pour associer les commits au compte GitHub.
$ git config --global user.email "<user>@yahoo.fr"
# Vérifier les paramètres saisis
$ git config --list

2°) Démarrer un dépôt Git

Vous pouvez principalement démarrer un dépôt Git de deux manières. La première consiste à prendre un projet ou un répertoire existant et à l'importer dans Git. La seconde consiste à cloner un dépôt Git existant sur un autre serveur.
Initialisation d'un dépôt Git dans un répertoire existant
Si vous commencez à suivre un projet existant dans Git, vous n'avez qu'à vous positionner dans le répertoire du projet et saisir :
$ git init
Cela crée un nouveau sous-répertoire nommé .git qui contient tous les fichiers nécessaires au dépôt — un squelette de dépôt Git. Pour l'instant, aucun fichier n'est encore versionné. 

Si vous souhaitez commencer à suivre les versions des fichiers existants (contrairement à un répertoire vide), vous devriez probablement commencer par indexer ces fichiers et faire une validation initiale. Vous pouvez réaliser ceci avec une poignée de commandes git add qui spécifient les fichiers que vous souhaitez suivre, suivie d'une validation :

$ git add <fichier>
$ git commit –m 'version initiale du projet'

Nous allons passer en revue ce que ces commandes font dans une petite minute. Pour l'instant, vous avez un dépôt Git avec des fichiers sous gestion de version et une validation initiale.
Cloner un dépôt existant : https://github.com/amowu/hello-ci-workflow.git

Si vous souhaitez obtenir une copie d'un dépôt Git existant — par exemple, un projet auquel vous aimeriez contribuer — la commande dont vous avez besoin s'appelle git clone.

3°) Créer un dépôt sur github
Cliquez sur “Create a free account” et suivez les instructions pour créer votre compte
Créer un compte GitHub sur https://github.com/plans
Créer un nouveau dépôt ou repository :
•	Nous allons maintenant créer un nouveau dépôt. Cliquez sur “Create a New Repo” dans la section à droite en haut du site.
 
•	Donnez un nom et une description à votre projet. Par défaut vous aurez un dépôt public et le projet sera vide à sa création. Nous pouvons y placer un fichier readme, en cochant la case “Initialize this project with a README”.
 
•	Maintenant que le dépôt est créé, vous pouvez le cloner en local, sur votre ordinateur. Lancez le programme GitHub que vous venez d’installer. Vous allez ajouter les informations GITHUB pour que le programme puisse accéder à votre compte. 
 

git add <fichier>
git add <dossier>
git status
git commit
git commit -m "message"
git remote add origin https://github.com/<user>/ ci-project.git
git push



