### Ce projet se nomme "Auth Database"

Le projet permet de creer des Users et stocker leurs informations dans une database postgreSQL, de securiser l'axxès avec l'authentification JWT et de l'API routing.

Le but initial du projet etait de faire 2 databases, une pour les Users et une avec des donnees auxquelles on aurait pu acceder par requete et en fournissant un user de la premiere database. J'ai du abandonner la partie avec les donnees lorsque j'ai voulu securiser les endpoints, pour une raison que je fournirai plus tard.

## Generation des Users

Il est possible de creer des Users et de les lire via APi endpoints. Ils sont gereres avec user_generator.py .

## Authentification avec JWT

Le but est de securiser les API endpoints avec JWT. Il faut donc pouvoir login et verifier les tokens que les users veulent envoyer.
Au final, nous utilisons le module "jwt" pour ce faire. Beaucoup de problèmes sont apparus avec le module "jose", que nous avons donc remplace. Il a ete impossible de lancer le projet avec docker compose avec le module jose, et c'est sur ce point que la majorite des difficultes ont ete rencontrees.

## Database

Un 2eme endpoint est la database persistente qui est pre-configuree pour accueillir les informations des Users : id, nom (name), email et mot de passe hashe avec sha256 sous la forme d'un string.

## Deploiement

Il faut s'assurer d'avoir Docker et Docker Compose. Ensuite, executer la commande "docker compose up --build" dans le cmd en etant dans le dossier app. 

Les conteneurs vont se lancer grâce au Dockerfile et docker-compose.yml. Les modules requis pour le fonctionnement de l'app sont dans le requirements.txt et sont automatiquement installes.

L'api FastAPI est host à l'adresse http://localhost:8000, tandis que la database run sur le port 5432.
