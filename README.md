# Projet "INSEE"

Projet de Master 1 en Biologie Computationnelle à L'université de Bordeaux, 2019-2020

Dans le cadre d'un projet en Bases de Données, nous nous sommes intéressés aux données sociales et environnementales pour les départements Français de 2008 à 2016. L'INSEE (Institut National Statistiques Études Économiques) publie régulièrement de nombreuses informations et a la charge du recensement de la population Française.

A l'aide du langage de programmation Python nous allons récupérer les différentes données qui ont été exportées dans des fichier CSV (Comma-separated values) et dans des fichiers Excel. Puis par la suite, nous allons les implémenter dans un système de gestion de base de données relationnelles et objet (SGBDRO). Une fois ce premier script réalisé, nous en développerons un second afin d'interagir avec cette Base de Données en effectuant des interrogations à partir d’un menu dans la console, avec une présentation facilitant la lecture.

Le but du projet est donc d’apprendre à stocker des informations dans une Base de Données par le biais de scripts Python, et par la suite de pouvoir les manipuler grâce à des requêtes SQL afin de répondre aux questions posées pour ce projet.

## Pour Commencer

Cette application a été développée en Python 3.7 avec la librairie Pandas.
La lecture du document **[projet_insee.pdf](projet_insee.pdf)** fourni tous les détails relatifs à cette application.

### Pré-requis

Les prérequis correspondant aux connaissances nécessaires et à l'environnement de développement sont les suivants :

* Python 3.7 avec Librairie Pandas
* un EDI, par exemple PyCharm, VSCode avec le module Python, Jypiter...
* Base de données SQL, dans notre cas PostgreSQL a été utilisé avec pgadmin pour la gestion

### Installation

Pour installer ce projet il faut :

* Installer PostgreSQL (ou autre)
* cloner le repository
* Executer le programme **read.py** pour construire la base de données et les charger
* Exécuter le programme **request.py** pour interroger la base et créer les fichiers html de réponse
  * note: les fichiers html sont créés par le code Python, ils sont fournis dans ce dépôt à titre indicatif

## Fabriqué avec

Les programmes/logiciels/ressources utilisés pour développer cette Application :

* [Anaconda](https://www.anaconda.com/products/individual) - Environnement Python
  * [Pandas](https://pandas.pydata.org/) - Librairie Pandas pour Python
* [PostgreSQL](https://www.postgresql.org/) - Moteur de base de données PostgreSQL
  * [pgAdmin 4](https://www.pgadmin.org/) - pgAdmin pour l'administration de PostgreSQL
* [Visual Studio Code](https://code.visualstudio.com/docs/languages/markdown) - VS Code et les extensions markdown pour la création de ce README.md

## Versions

Versions disponible :

* **Dernière version :** 1.0

## Auteur

Application développée par :

* **Alexandre Cornier** _alias_ [@alexcornier](https://github.com/alexcornier/)

## License

Ce projet est sous licence ``MIT License`` - voir le fichier [LICENSE.md](LICENSE.md) pour plus d'informations.
