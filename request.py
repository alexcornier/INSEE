#================================================================
# Ensemble de requêtes SQL sur une base de données SQL
# hébergées sur un serveur local postgresql
#
# Modules pythons nécessaires
#   psycopg2 (SQL connection)
#   pandas (DataFrame et HTML)
#   matplotlib
#   jinja2 (styles HTML)
#
# Alexandre Cornier - 2020
#================================================================

import psycopg2
import pandas as pd
import webbrowser
import pathlib

# Interrupteur d'affichage console
bconsole = False # pas d'affichage console par défaut

#---------------------------- Connection à la Base de Données ------------------------------------
connection = psycopg2.connect("host=localhost port=5432 dbname=cremi user=postgres password=Audierne")
cur = connection.cursor()

#-------------------------------------- Fonctions ------------------------------------------------

# Affichage HTML des résultats dans le navigateur
def affiche_html(titre_question, question, fichier, resultat_html):
    # Préparation de l'entête du fichier HTML
    header = """<!DOCTYPE html>
    <html>
    <head>
    <title>""" + titre_question + """</title>
    </head>
    <body>
    
    <h1>""" + titre_question + """</h1>
    <p>""" + question + """</p>
    """

    footer = """
    </body>
    </html>"""

    # write html to file
    text_file = open(fichier, "w")
    text_file.write(header)
    text_file.write(resultat_html)
    text_file.write(footer)
    text_file.close()

    # open report.html in browser
    current_path = pathlib.Path(__file__).parent.absolute()
    fichier = "file://" + str(current_path) + "/" + fichier
    webbrowser.open(fichier)


# Question 1
def listeRegions():
    cur.execute("""SELECT reg, libelle FROM regions ORDER BY reg""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Code région', 'Région'])

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Région" else '' for i in x])
        .hide_index()
        .render())

    affiche_html("Question 1", "Régions présentes dans la base de données",\
                 "question_01.html", html)

    if (bconsole):
        print("les régions présentes dans la base de données sont : ")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 2
def listeDepartement():
    cur.execute("""SELECT dep, libelle FROM departements ORDER BY dep""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Code département', 'Département'])

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Département" else '' for i in x])
        .hide_index()
        .render())

    affiche_html("Question 2", "Départements présents dans la base de données",\
                 "question_02.html", html)

    if (bconsole):
        print("les départements présents dans la base de données sont : ")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 3
def choixRegions():
    print("Donnez le nom de la région :")
    choix = input().capitalize()
    cur.execute("""SELECT * FROM regionsocial WHERE region = '%s' """ % choix)

    lst = []
    for info in cur.fetchall():
        lst=[["Numéro", info[0]],
               ["Taux de pauvreté (%)", info[2]],
               ["Part des jeunes non insérés (%) en 2014", info[3]],
               ["Part des jeunes non insérés (%) en 2009", info[4]],
               ["Poids de l'économie sociale dans les emplois salariés du territoire (%)", info[5]]]

    df = pd.DataFrame(lst, columns=['Information', 'Valeur'])

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .set_properties(subset=["Valeur"], **{'text-align': 'right'})
        .hide_index()
        .render())

    affiche_html("Question 3", "Informations concernant la régione " + choix,\
                 "question_03.html", html)

    if (bconsole):
        print("-------------- Informations concernant", choix, "--------------")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 4
def choix_departement_theme(): 
    print("Donnez le nom du département :")
    choix1 = input().capitalize()
    print("Choisissez un thème : 1.Social ou 2.Environnement (par défaut)")
    choix2 = input()

    lst = []
    if choix2 == "1" or choix2.lower() == "social":
        cur.execute("""SELECT * FROM departementsocial WHERE departements = '%s' """ % choix1)

        for info in cur.fetchall():
            lst = [["Numéro", info[0]],
                    ["Espérance de vie des hommes à la naissance en 2015 (années)", info[2]],
                    ["Espérance de vie des hommes à la naissance en 2010 (années)", info[3]],
                    ["Espérance de vie des femmes à la naissance en 2015 (années)", info[4]],
                    ["Espérance de vie des femmes à la naissance en 2010 (années)", info[5]],
                    ["Part de la population éloignée de plus de 7 mn des services de santé de proximité (%) en 2016", info[6]],
                    ["Part de la population estimée en zone inondable (%)", info[7]]]

        df = pd.DataFrame(lst, columns=['Information', 'Valeur'])

        df["Valeur"] = pd.to_numeric(df["Valeur"], errors='coerce')

        html = (df.style
            .set_table_styles([
                {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
                {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
                {'selector': 'th', 'props': [
                    ('background', '#606060'),
                    ('color', 'white'),
                    ('font-family', 'verdana')]},
                {'selector': 'td', 'props': [('font-family', 'verdana')]}])
            .format({"Valeur": "{:.1f}"})
            .set_properties(subset=["Valeur"], **{'text-align': 'right'})
            .hide_index()
            .render())

        affiche_html("Question 4a",\
                     "Informations sociales concernant le département " + choix1,\
                     "question_04a.html", html)

        if (bconsole):
            df["Valeur"] = df["Valeur"].map("{:.1f}".format)
            print("-------------- Informations concernant", choix1, "--------------")
            print(df)

    else :
        cur.execute("""SELECT * FROM departementenvironnement WHERE departements = '%s' """ % choix1)

        for info in cur.fetchall():
            lst = [["Numéro", info[0]],
            ["Taux de valorisation matière et organique (%) en 2013", info[2]],
            ["Taux de valorisation matière et organique (%) en 2009", info[3]],
            ["Part de surfaces artificialisées (%) en 2012", info[4]],
            ["Part de surfaces artificialisées (%) en 2006", info[5]],
            ["Part de l'agriculture biologique dans la surface agricole totale (%) en 2016", info[6]],
            ["Part de l'agriculture biologique dans la surface agricole totale (%) en 2010", info[7]],
            ["Production de granulats (tonnes) en 2014", info[8]],
            ["Production de granulats (tonnes) en 2009", info[9]],
            ["Eolien (%) en 2015", info[10]],
            ["Eolien (%) en 2010", info[11]],
            ["Photovoltaïque (%) en 2015", info[12]],
            ["Photovoltaïque (%) en 2010", info[13]],
            ["Autre (biogaz, biomasse, géothermie, incinération de déchets, petite hydraulique) (%) en 2015",info[14]],
            ["Autre (biogaz, biomasse, géothermie, incinération de déchets, petite hydraulique) (%) en 2010",info[15]]]

        df = pd.DataFrame(lst, columns=['Information', 'Valeur'])

        df["Valeur"] = pd.to_numeric(df["Valeur"], errors='coerce')

        html = (df.style
            .set_table_styles([
                {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
                {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
                {'selector': 'th', 'props': [
                    ('background', '#606060'),
                    ('color', 'white'),
                    ('font-family', 'verdana')]},
                {'selector': 'td', 'props': [('font-family', 'verdana')]}])
            .format({"Valeur": "{:.1f}"})
            .set_properties(subset=["Valeur"], **{'text-align': 'right'})
            .hide_index()
            .render())

        affiche_html("Question 4b",\
                     "Informations environnementales concernant le département " + choix1,\
                     "question_04b.html", html)

        if (bconsole):
            df["Valeur"] = df["Valeur"].map("{:.1f}".format)
            print("-------------- Informations concernant", choix1, "--------------")
            print(df)

    if (bconsole):
        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 5
def typeEnergie():
    print("Choisissez un type d'energie : 1.Eolien, 2.Photovoltaique ou 3.Autre")
    choix = input()

    if choix == "1" or choix.lower() == "eolien":
            cur.execute("""SELECT nb, departements, eolien2015 - eolien2010 AS croissance FROM departementenvironnement
                WHERE eolien2015 > eolien2010
                ORDER BY eolien2015 - eolien2010 DESC""")
            query_result = cur.fetchall()
            df = pd.DataFrame(query_result, columns=['Code', 'Département', 'Croissance'])

            html = (df.style
                .set_table_styles([
                    {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
                    {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
                    {'selector': 'th', 'props': [
                        ('background', '#606060'),
                        ('color', 'white'),
                        ('font-family', 'verdana')]},
                    {'selector': 'td', 'props': [('font-family', 'verdana')]}])
                .apply(lambda x: ['background: lightblue' if x.name == "Département" else '' for i in x])
                .background_gradient(cmap='Blues', subset=["Croissance"])
                .format({"Croissance": "{:.1f}pts"})
                .set_properties(subset=["Croissance"], **{'text-align': 'right'})
                .hide_index()
                .render())

            affiche_html("Question 5a",\
                         "Départements où la part de l'énergie éolienne a augmenté entre les deux années de référence",\
                         "question_05a.html", html)

            if (bconsole):
                df["Croissance"] = df["Croissance"].map("{:.1f}pts".format)
                print(
                    "Voici la liste des départements où la part de cette énergie a augmenté entre les deux années de référence : ")
                print(df)

    if choix == "2" or choix.lower() == "photovoltaique":
            cur.execute("""SELECT nb, departements, photovoltaique2015 - photovoltaique2010 AS croissance FROM departementenvironnement
                WHERE photovoltaique2015 > photovoltaique2010
                ORDER BY photovoltaique2015 - photovoltaique2010 DESC""")
            query_result = cur.fetchall()
            df = pd.DataFrame(query_result, columns=['Code', 'Département', 'Croissance'])

            html = (df.style
                .set_table_styles([
                    {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
                    {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
                    {'selector': 'th', 'props': [
                        ('background', '#606060'),
                        ('color', 'white'),
                        ('font-family', 'verdana')]},
                    {'selector': 'td', 'props': [('font-family', 'verdana')]}])
                .apply(lambda x: ['background: lightblue' if x.name == "Département" else '' for i in x])
                .background_gradient(cmap='Blues', subset=["Croissance"])
                .format({"Croissance": "{:.1f}pts"})
                .set_properties(subset=["Croissance"], **{'text-align': 'right'})
                .hide_index()
                .render())

            affiche_html("Question 5b",\
                         "Départements où la part de l'énergie photovoltaïque a augmenté entre les deux années de référence",\
                         "question_05b.html", html)

            if (bconsole):
                df["Croissance"] = df["Croissance"].map("{:.1f}pts".format)
                print("Voici la liste des départements où la part de cette énergie a augmenté entre les deux années de référence : ")
                print(df)

    if choix == "3" or choix.lower() == "autre":
            cur.execute("""SELECT nb, departements, autre2015 - autre2010 AS croissance FROM departementenvironnement
                WHERE autre2015 > autre2010
                ORDER BY autre2015 - autre2010 DESC""")
            query_result = cur.fetchall()
            df = pd.DataFrame(query_result, columns=['Code', 'Département', 'Croissance'])

            html = (df.style
                .set_table_styles([
                    {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
                    {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
                    {'selector': 'th', 'props': [
                        ('background', '#606060'),
                        ('color', 'white'),
                        ('font-family', 'verdana')]},
                    {'selector': 'td', 'props': [('font-family', 'verdana')]}])
                .apply(lambda x: ['background: lightblue' if x.name == "Département" else '' for i in x])
                .background_gradient(cmap='Blues', subset=["Croissance"])
                .format({"Croissance": "{:.1f}pts"})
                .set_properties(subset=["Croissance"], **{'text-align': 'right'})
                .hide_index()
                .render())

            affiche_html("Question 5c",\
                         "Départements où la part des énergies renouvelables autres a augmenté entre les deux années de référence",\
                         "question_05c.html", html)

            if (bconsole):
                df["Croissance"] = df["Croissance"].map("{:.1f}pts".format)
                print("Voici la liste des départements où la part de cette énergie a augmenté entre les deux années de référence : ")
                print(df)

    if (bconsole):
        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 6
def tonnes():
    cur.execute("""SELECT departements.reg, regions.libelle AS region, departements.libelle AS departement
        FROM departements, regions 
        WHERE departements.reg
        IN (SELECT departements.reg from departements
            INNER JOIN departementenvironnement
            ON departements.dep = departementenvironnement.nb
            INNER JOIN regions
            ON departements.reg = regions.reg
            GROUP BY departements.reg
			HAVING SUM(prodgranulat2014) > 25000000
			AND SUM(prodgranulat2014) <> 'NaN')
		ORDER BY region, departement""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Code région', 'Région', 'Département'])

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Département" else '' for i in x])
        .hide_index()
        .render())

    affiche_html("Question 6",\
                 "Départements dont la région a eu une production de granulats supérieure à 25 000 000 tonnes en 2014",\
                 "question_06.html", html)

    if (bconsole):
        print("les départements dont la région a eu une production de granulats supérieure à 25 000 000 tonnes en 2014 sont :")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 7
def topFive():
    cur.execute("""SELECT nb, departements, eolien2015 FROM departementenvironnement 
        ORDER BY nullif(eolien2015, 'NaN')
        DESC nulls last LIMIT 5""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Code département', 'Département', "Part de l'énergie éolienne en 2015"])

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Département" else '' for i in x])
        .background_gradient(cmap='Blues', subset=["Part de l'énergie éolienne en 2015"])
        .format({"Part de l'énergie éolienne en 2015": "{:.1f}%"})
        .set_properties(subset=["Part de l'énergie éolienne en 2015"], **{'text-align': 'right'})
        .hide_index()
        .render())

    affiche_html("Question 7",\
                 "Les 5 départements avec le plus grand taux d’énergie éolienne comme source de la puissance électrique en 2015",\
                 "question_07.html", html)

    if (bconsole):
        df["Part de l'énergie éolienne en 2015"] = df["Part de l'énergie éolienne en 2015"].map("{:.1f}%".format)
        print("Les 5 départements avec le plus grand taux d’énergie éolienne comme source de la puissance électrique en 2015 sont :")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 8
def weak():
    cur.execute("""SELECT regions.reg, regions.libelle AS region,
        departements.libelle AS departement, departementenvironnement.valorisationorga2013
        FROM departements
        INNER JOIN regions
        ON departements.reg = regions.reg
        INNER JOIN departementenvironnement
        ON departements.dep = departementenvironnement.nb
        ORDER BY nullif(valorisationorga2013, 'NaN') nulls last LIMIT 1""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Code région', 'Région', 'Département', 'Valorisation en 2013'])

    # Formattage des valeurs
    df["Valorisation en 2013"] = df["Valorisation en 2013"].map("{:.1f}".format)

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Région" else '' for i in x])
        .set_properties(subset=["Valorisation en 2013"], **{'text-align': 'right'})
        .hide_index()
        .render())

    affiche_html("Question 8",\
                 "Région où se trouve le département ayant le plus faible taux de valorisation matière et organique en 2013",\
                 "question_08.html", html)

    if (bconsole):
        print("La région où se trouve le département ayant le plus faible taux de valorisation matière et organique en 2013 est :")
        print("Reg, Région, Département, Valorisation2013")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 9
def bestPopMin():
    cur.execute("""SELECT departementenvironnement.departements, departementenvironnement.agriculturebio2016 
        FROM departementenvironnement
        INNER JOIN departementsocial
        ON departementenvironnement.departements = departementsocial.departements
        ORDER BY nullif(popeloignee7min, 'NaN') DESC nulls last LIMIT 1""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Département', "Part de l'agriculture biologique"])

    # Formattage des valeurs
    df["Part de l'agriculture biologique"] = df["Part de l'agriculture biologique"].map("{:.1f}%".format)

    titre_html = "Part en 2016 (en %) de l’agriculture biologique dans la surface agricole totale du département<br>" +\
    "contenant le plus grand pourcentage de population éloignée de plus de 7 minutes des services de santé de proximité"

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Part de l'agriculture biologique" else '' for i in x])
        .set_properties(subset=["Part de l'agriculture biologique"], **{'text-align': 'right'})
        .hide_index()
        .render())

    affiche_html("Question 9", titre_html, "question_09.html", html)

    if (bconsole):
        print("En 2016, la part (en %) de l’agriculture biologique dans la surface agricole totale du département")
        print("contenant le plus grand pourcentage de population éloignée de plus de 7 minutes des services de santé de proximité est : ")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 10
def pauvrete():
    cur.execute("""SELECT pauvrete,region 
        FROM regionsocial 
        WHERE jeunesnoninseres2014 > 30
        AND pauvrete <> 'NaN'
        ORDER BY nullif(pauvrete, 'NaN') DESC nulls last""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Pauvreté', 'Région'])

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .apply(lambda x: ['background: lightblue' if x.name == "Pauvreté" else '' for i in x])
        .format({"Pauvreté": "{:.2f}%"})
        .set_properties(subset=["Pauvreté"], **{'text-align': 'right'})
        .hide_index()
        .render())

    affiche_html("Question 10",\
                 "Taux de pauvreté connu en 2014 des régions dont la part des jeunes non insérés est supérieure à 30% en 2014",\
                 "question_10.html", html)

    if (bconsole):
        df["Pauvreté"] = df["Pauvreté"].map("{:.2f}%".format)
        print("Le taux de pauvreté connu en 2014 des régions dont la part des jeunes non insérés est supérieure à 30% en 2014 sont : ")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


# Question 11
def poids_eco():
    cur.execute("""SELECT regions.reg, regions.libelle, poidseco,
        AVG(photovoltaique2015) AS photovoltaique2015,
        AVG(agriculturebio2016) AS agriculturebio2016
        FROM departements
        INNER JOIN departementenvironnement
            ON departements.dep = departementenvironnement.nb
        INNER JOIN regionsocial
            ON departements.reg = regionsocial.nb
        INNER JOIN regions
            ON departements.reg = regions.reg
        GROUP BY poidseco, regions.reg
            HAVING AVG(photovoltaique2015) >= 10
                AND AVG(photovoltaique2015) <> 'NaN'
                AND AVG(agriculturebio2016) >= 5
                AND AVG(agriculturebio2016) <> 'NaN'
        ORDER BY poidseco""")
    query_result = cur.fetchall()
    df = pd.DataFrame(query_result, columns=['Code région', 'Région', "Poids de l'économie sociale",\
                                             "Part moyenne du photovoltaïque", "Part moyenne de l'agriculture Bio"])

    # Conversion string vers float pour le formattage
    df["Part moyenne du photovoltaïque"] = pd.to_numeric(df["Part moyenne du photovoltaïque"], errors='coerce').fillna(0)
    df["Part moyenne de l'agriculture Bio"] = pd.to_numeric(df["Part moyenne de l'agriculture Bio"], errors="coerce").fillna(0)

    titre_html = "Poids de l'économie sociale en 2015 dans les emplois salariés de la région<br>" +\
    "dont la source de la puissance électrique en énergies renouvelables provenait à au moins 10% de l'énergie photovoltaïque<br>" +\
    "et dont la part de l'agriculture biologique dans la surface agricole totale était d'au moins 5%"

    html = (df.style
        .set_table_styles([
            {'selector': 'tr:nth-of-type(odd)', 'props': [('background', '#eee')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background', 'white')]},
            {'selector': 'th', 'props': [
                ('background', '#606060'),
                ('color', 'white'),
                ('font-family', 'verdana')]},
            {'selector': 'td', 'props': [('font-family', 'verdana')]}])
        .set_properties(subset=["Poids de l'économie sociale", "Part moyenne du photovoltaïque",
                                "Part moyenne de l'agriculture Bio"], **{'text-align': 'right'})
        .hide_index()
        .background_gradient(cmap='Blues', subset=["Poids de l'économie sociale"])
        .format({"Poids de l'économie sociale": "{:.1f}%"})
        .format({"Part moyenne du photovoltaïque": "{:.1f}%"})
        .format({"Part moyenne de l'agriculture Bio": "{:.1f}%"})
        .render())

    affiche_html("Question 11", titre_html, "question_11.html", html)

    if (bconsole):
        df["Poids de l'économie sociale"] = df["Poids de l'économie sociale"].map("{:.1f}%".format)
        df["Part moyenne du photovoltaïque"] = df["Part moyenne du photovoltaïque"].map("{:.1f}%".format)
        df["Part moyenne de l'agriculture Bio"] = df["Part moyenne de l'agriculture Bio"].map("{:.1f}%".format)
        print("Poids de l'économie sociale en 2015 dans les emplois salariés de la région")
        print("dont la source de la puissance électrique en énergies renouvelables provenait à au moins 10% de l'énergie photovoltaïque")
        print("et dont la part de l'agriculture biologique dans la surface agricole totale était d'au moins 5%")
        print(df)

        print("Appuyez sur entrée pour revenir au menu")
        input()


def menu():
    print ("")
    print ("------------------------------------ Projet INSEE -----------------------------------")
    print ("")
    print ("1...Afficher la liste des régions")
    print ("2...Afficher la liste des départements")
    print ("3...Demander à l’utilisateur de choisir une région et afficher les données de la region choisie")
    print ("4...Demander à l’utilisateur de choisir un département et un thème : social ou environnemental,")
    print ("      | et afficher les données demandées pour le departement choisi")
    print ("5...demander à l’utilisateur de choisir un type d’énergie (éolien, photovoltaïque, autre)")
    print ("      | et en fonction de ce choix retourner la liste des départements où la part de cette énergie a augmenté")
    print ("      | entre les deux années de référence, classés de la plus forte augmentation à la plus faible.")
    print ("6...les départements dont la région a eu une production de granulats supérieure à 25 000 000 tonnes en 2014")
    print ("7...les 5 départements avec le plus grand taux d’énergie éolienne comme source de la puissance électrique en 2015")
    print ("8...La région où se trouve le département ayant le plus faible taux de valorisation matière et organique en 2013")
    print ("9...La part (en %) de l’agriculture biologique dans la surface agricole totale du département contenant")
    print ("      | le plus grand pourcentage de population éloignée de plus de 7 minutes des services de santé de proximité en 2016")
    print ("10..Le taux de pauvreté en 2014 des régions dont la part des jeunes non insérés est supérieure à 30% en 2014 ")
    print ("11..Le poids de l'économie sociale dans les emplois salariés de la région dont la source de la puissance électrique")
    print ("      | en énergies renouvelables provenait à au moins 10% de l’énergie photovoltaïque et dont la part")
    print ("      | de l’agriculture biologique dans la surface agricole totale était d’au moins 5% en 2015")
    print ("")
    print ("0...Quitter")
    print ("-------------------------------------------------------------------------------------")


#----------------------------------------- MAIN --------------------------------------------------

# Demande d'affichae console ou non, HTML seul par défaut

print("Souhaitez-vous afficher les résultats dans la console,")
print("en plus de la création des fichiers HTML ?")
print("   (O Oui / N Non)")
choix = input()

if (choix[0].lower() == "o"):
    bconsole = True

# Menu principal

while True:
    menu()
    print("Chosissez un numéro de question pour avoir la réponse :")
    choix = input()

    if (choix == "1"):
        listeRegions()
    elif (choix == "2"):
        listeDepartement()
    elif (choix == "3"):
        choixRegions()
    elif (choix == "4"):
        choix_departement_theme()
    elif (choix == "5"):
        typeEnergie()
    elif (choix == "6"):
        tonnes()
    elif (choix == "7"):
        topFive()
    elif (choix == "8"):
        weak()
    elif (choix == "9"):
        bestPopMin()
    elif (choix == "10"):
        pauvrete()
    elif (choix == "11"):
        poids_eco()
    elif (choix == "0"):
        break
    else:
        print ("Choix invalide")

# fermeture "propre" du curseur et de la connection
cur.close()
connection.close()