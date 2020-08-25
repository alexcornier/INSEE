# ================================================================
# Construction et chargement d'une base de données SQL
# hébergées sur un serveur local postgresql
#
# Modules pythons nécessaires
#   psycopg2 (SQL connection)
#   csv
#   pandas (DataFrame et HTML)
#   numpy
#
# Alexandre Cornier - 2020
# ================================================================

import psycopg2
import csv
import pandas as pd
import numpy as np

# ------------------------------------- DATABASE -------------------------------------
connection = psycopg2.connect("host=localhost port=5432 user=postgres")

# Configuration du niveau d'isolation en autocommit pour eviter une erreur
connection.autocommit = True

# Creation du curseur
cur = connection.cursor()

# Creation d'une nouvelle base de donnes pour le CREMI
cur.execute("CREATE DATABASE cremi")

# Fermeture dur curseur et de la connection et reouverture sur la nouvelle base de donnees
cur.close()
connection.close()
connection = psycopg2.connect("host=localhost port=5432 dbname=cremi user=postgres")
cur = connection.cursor()

# ------------------------------------ PARTIE CSV ------------------------------------
# TABLE departements :
#   - creation de la table dans le psql
#   - lecture du fichier *.csv dans python
#   - Insertion des datas dans la table departements

cur.execute("""
    CREATE TABLE departements(
    dep text PRIMARY KEY,
    reg text,
    cheflieu text,
    tncc text,
    ncc text,
    nccenr text,
    libelle text)
""")

file = open("departement2020.csv", encoding="utf8")
reader = csv.reader(file, delimiter=",")

# Permet de retirer l'entete
next(reader)

for row in reader:
    cur.execute(
    "INSERT INTO departements VALUES (%s, %s, %s, %s, %s, %s, %s)",
    row
    )
connection.commit()
file.close()

# TABLE regions :
#   - creation de la table dans le psql
#   - lecture du fichier *.csv dans python
#   - Insertion des datas dans la table regions

cur.execute("""
    CREATE TABLE regions(
    reg text PRIMARY KEY,
    cheflieu text,
    tncc integer,
    ncc text,
    nccenr text,
    libelle text)
""")

file=open("region2020.csv", encoding="utf8") # utf8 pour résoudre d'éventuels problèmes d'accents
reader = csv.reader(file, delimiter = ",")
next(reader)

for row in reader:
    cur.execute(
    "INSERT INTO regions VALUES (%s, %s, %s, %s, %s, %s)",
    row
    )
connection.commit()
file.close()

# ------------------------------------ PARTIE XLSX ------------------------------------
# TABLE regionsocial :
#   - creation de la table dans le psql
#   - lecture du fichier *.xlsx dans python
#   - Insertion des datas dans la table regionssocial

cur.execute("""
    CREATE TABLE regionsocial(
    nb text PRIMARY KEY,
    region text,
    pauvrete float,
    jeunesnoninseres2014 float,
    jeunesnoninseres2009 float,
    poidseco float)
""")

myFile = 'DD-indic-reg-dep_janv2018.xls'
df1 = pd.read_excel(myFile, sheet_name='Social', usecols="A:F",skiprows=3,nrows=21,header=None)
df1.replace(["nd", "nd ", "nc", "nc"], np.NaN, inplace = True)

for i in range (len(df1)):
    linesRegions = df1.iloc[i]
    cur.execute(
    "INSERT INTO regionsocial VALUES (%s, %s, %s, %s, %s, %s)",
    linesRegions
    )

connection.commit()

# TABLE departementsocial :
#   - creation de la table dans le psql
#   - lecture du fichier *.xlsx dans python
#   - Insertion des datas dans la table departementsocial

cur.execute("""
    CREATE TABLE departementsocial(
    nb text PRIMARY KEY,
    departements text,
    esphommes2015 text,
    esphommes2010 float,
    espfemmes2015 float,
    espfemmes2010 float,
    popeloignee7min float,
    popzoneinondable2013 float,
    popzoneinondable2008 float)
""")

myFile = 'DD-indic-reg-dep_janv2018.xls'
df2 = pd.read_excel(myFile, sheet_name='Social', usecols="A:I",skiprows=28,nrows=104,header=None)
df2.replace(["nd", "nd ", "nc", "nc"], np.NaN, inplace = True)

for i in range (len(df2)):
    linesDepartement = df2.iloc[i]
    cur.execute(
    "INSERT INTO departementsocial VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    linesDepartement
    )

connection.commit()

# TABLE departementenvironnement :
#   - creation de la table dans le psql
#   - lecture du fichier *.xlsx dans python
#   - Insertion des datas dans la table departementenvironnement

cur.execute("""
    CREATE TABLE departementenvironnement(
    nb text PRIMARY KEY,
    departements text,
    valorisationorga2013 float,
    valorisationorga2009 float,
    surfacearti2012 float,
    surfacearti2006 float,
    agriculturebio2016 float,
    agriculturebio2010 float,
    prodgranulat2014 float,
    prodgranulat2009 float,
    eolien2015 float,
    eolien2010 float,
    photovoltaique2015 float,
    photovoltaique2010 float,
    autre2015 float,
    autre2010 float)
""")

myFile = 'DD-indic-reg-dep_janv2018.xls'
df3 = pd.read_excel(myFile, sheet_name='Environnement', usecols="A:P",skiprows=3,nrows=104,header=None)
df3.replace(["nd", "nd ", "nc", "nc"], np.NaN, inplace = True)

for i in range (len(df3)):
    linesdepartementEnv = df3.iloc[i]
    cur.execute(
    "INSERT INTO departementenvironnement VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    linesdepartementEnv
    )

connection.commit()

# ------------------------------ PREPARATION DES DONNEES ------------------------------

# TABLE departements :
#   - Ajout d'un 0 devant les numéros de départements < 10 pour aligner
#     les valeurs de la table departements venant du fichier CSV avec
#     departementenvironnement et departementsocial issus du fichier Excel

cur.execute("""
    UPDATE departements
    SET dep = CONCAT('0', dep)
    WHERE dep LIKE '_';
""")

connection.commit()

# TABLE departements :
#   - Ajout d'un 0 devant les numéros de régions < 10 pour aligner
#     avec les valeurs de la table régions venant du fichier CSV avec

cur.execute("""
    UPDATE departements
    SET reg = CONCAT('0', reg)
    WHERE dep LIKE '_';
""")

connection.commit()

# fermeture "propre" du curseur et de la connection
cur.close()
connection.close()