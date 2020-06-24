'''
CREATION D'UNE APPLICATION WEB NUTRITIONNELLE

Cette application a pour objectif de permettre à un utilisateur d'avoir des
recommandations alimentaires en fonction de sa consommation personnelle,
qu'il soit sportif ou non. On lui proposera des recettes en fonction de son
bilan nutritionel.
L'utilisateur aura aussi la possibilité d'avoir des renseignements sur les
fruits et légumes de saisons, sur l'alimentation BIO, et les valeurs nutritives
des aliments.

'''

# Librairies externes
from flask import Flask , render_template, redirect, url_for, flash, session
from flask import request, Response
import numpy as np
import datetime as date
import random as rd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlite3 as lite
from werkzeug.security import generate_password_hash, check_password_hash

########### Import pour autocompletion #######################################

import json
from wtforms import TextField, Form
from saisonnalite import *
from liste_aliments import *
##############################################################################


# Librairies internes au projet
from graphiques import generateur_historique_repas, rendu_graphique
from graphiques import generateur_repas, carences, date_aleatoire,valeur_repas
from graphiques import bilan_nutritionnel, valeur_nutrition_sur_nbJours
import liste_aliments, saisonnalite
ADRESSE_BASE_DE_DONNEES = "base_fictive.db"
ADRESSE_BDD_AUTH = "test116.db"



# Initialisation de l'application web avec Flask
app=Flask(__name__)



@app.route('/')
def info():

    title = "Accueil"
    return render_template("index.html", title=title)

@app.route('/liste_aliments')
def aliments():
    title = "liste_aliments"
    return render_template("liste_aliments.html", title=title,
    liste_allergies = liste_aliments.liste_allergies,
    liste_viandes = liste_aliments.liste_viandes,
    liste_legumes = liste_aliments.liste_legumes,
    liste_fruits = liste_aliments.liste_fruits,
    liste_fromages = liste_aliments.liste_fromages)



@app.route('/formulaire_graphe')
def formulaire_graphe():
    '''sur cette page l'utilisateur devra remplir un formulaire de type
       date et methode post qui lui permetera de choisir la période d'analyse souhaitée
       la date par défaut est obtenu grace à datetime
    '''

    graphs = ['repas','bilan', 'carence']
    date_debut =  date.datetime(2020,1,1)

    return render_template("formulaire_graphe.html",graphs=graphs
                           ,date_debut=date_debut)


@app.route('/graph_aliments', methods=['GET', 'POST'])
def graph():

    date_1, date_2 = date.datetime(2020, 1, 1), date.datetime(2020, 12, 31)
    date_debut = date.datetime(2020,1,1)
    date_fin = date.datetime(2020,6,7)
    utilisateur = "Lea"
    #mode = "repas"
    mode = request.form['graph']

    # les if déterminent le type de graphique souhaité à la page précédente.
    # selon le type de graphe choisi
    if mode == "repas":
        rendu_graphique(utilisateur, mode, date_debut, date_fin, date_1)
        image = "images/graph_repas.png"

    if mode == "bilan":
        rendu_graphique(utilisateur, mode, date_debut, date_fin, date)
        image= "images/graph_bilan.png"

    if mode == "carence":
        rendu_graphique(utilisateur, mode, date_debut,date_fin, date)
        image= "images/graph_carence.png"

    return render_template("graph_aliments.html", image = image)

@app.route('/recettes',methods=['GET', 'POST'])
def recettes():

    title = "recettes"
    return render_template("recettes.html", title=title)


@app.route('/saisonnalite', methods=['GET', 'POST'])
def saison():

    title = "saisonnalite"
    return render_template("saisonnalite.html", title=title,
    liste_fruits=saisonnalite.select_fruits,
    liste_legumes=saisonnalite.select_legumes,
    saison=saisonnalite.saison)


@app.route('/alimentation_bio',methods=['GET', 'POST'])
def bio():

    title = "alimentation_bio"
    return render_template("alimentation_bio.html", title=title)

@app.route('/menu_sportif')
def sportif():

    title = "menu_sportif"
    return render_template("menu_sportif.html", title=title)

@app.route('/creation_compte')
def creation_compte():
    """Ici nous envoyons une template qui permet la creation d'un compte.
       les informations nécéssaires sont les suivante : un nom de compte
       une addresse mail, et le mot de passe désiré en double"""
    if 'nom_de_compte' in session :
        return redirect("/")
    return render_template("formulaire_creation_compte.html")

@app.route('/traitement_creation_compte', methods=['POST'])
def traitement_creation_compte() :
    """Nous traiton le contenu du formulaire obtenu de la page de création
       Il est a noté que par sécurité le mot de passe de l'utilisateur ne doit
       JAMAIS être stocké sur la BDD en clair, et de limité au maximum les
       sotckage en variable en clair, si la requête est fait en HTTPS le mdp
       sera stocké au sein du formulaire encodé et donc ne sera jamais present
       sur le site sous quelque forme que ce soit en clair"""

    #Recuperation données formulaire
    nom_de_compte = request.form['nom_de_compte']
    mail = request.form['mail']

    #Verification que les mdp sont les même
    if request.form['mot_de_passe_1'] != request.form['mot_de_passe_2'] :
        return redirect("erreur_mdp")

    #Debut des operation
    con=lite.connect(ADRESSE_BDD_AUTH)
    with con:
        #Obtenir l'id par raport au dernier utilisateur
        df = pd.read_sql_query(f"""SELECT * FROM authentification
                                   ORDER BY id_auth DESC LIMIT 1""",con)
        id_auth = df['id_auth'][0] + 1

        #Verifion si le compte existe deja pour cela on récupère les resultat
        #D'une querry pour le nom du compte dans une dataframe panda
        df = pd.read_sql_query(f"""SELECT DISTINCT nom_de_compte
                                   FROM authentification
                                   WHERE nom_de_compte = '{nom_de_compte}'"""
                                                                        , con)
        #si la querry a donné 0 resultat le compte n'existe donc pas
        if df.empty:
            #Si non sallage du mot de passe avec werkzeug security
            mot_de_passe_sale = generate_password_hash(
                                                request.form['mot_de_passe_1'])
            cur = con.cursor()
            requete_SQL = f"""
                INSERT INTO authentification VALUES('{id_auth}',
                                                    '{nom_de_compte}',
                                                    '{mail}',
                                                    '{mot_de_passe_sale}')"""
            cur.execute(requete_SQL)
            cur.close()
            #Comunique a l'utilisateur le succès
            return redirect('/creation_success')
        #Si le compte existe deja redirige vers une page qui indique l'echec
        #de sa tentative de creation de compte
        return redirect('/creation_fail')

@app.route('/creation_fail')
def creation_fail() :
    return render_template('message_creation_fail.html')


@app.route('/creation_success')
def creation_success() :
    return render_template('message_creation_success.html')

#----- Connexion vers un compte ---------------------------------------->

@app.route('/formulaire_authentification')
def authentification():
    if 'nom_de_compte' in session :
        return redirect("/")
    "Le formulaire de connexion se contente de récupéré l'adresse et le mdp"
    return render_template("formulaire_authentification.html")


@app.route('/traitement_authentification', methods=['POST'])
def traitement_authentification():
    """ traitement des informations d'authentification et connexion de
    l'utilisateur. Les mêmes vérifications que pour un changement de mot de
    passe sont réalisées. Si le formulaire passe ces vérifications alors
    l'utilisateur est rajouté dans la "session" flask comme utilisateur
    et une page est renvoyée avec un cookie qui permet d'identifier
    l'utilisateur. Ces deux chose sont équivalente il sera possible donc de
    traquer l'individu soit sur les valeurs contenu dans "sa" session ou
    dans le cookie

    Une session est un cookie flask que l'utilisateur porte dans toutes ses
    étapes, le cookie est l'équivalent manuel. """

    mail = request.form['mail']
    con=lite.connect(ADRESSE_BDD_AUTH)
    with con:
        #Nou
        df=pd.read_sql_query(f'''SELECT DISTINCT mail FROM authentification
                                 WHERE mail = "{mail}"''', con)

        #Verifie si le compte existe deja
        if not df.empty:
            df=pd.read_sql_query(f'''SELECT DISTINCT mot_de_passe
                                     FROM authentification
                                     WHERE mail = "{mail}"''', con)
            #Verifie si le mot de passe est le bon
            if check_password_hash(df['mot_de_passe'][0],
                                   request.form['mot_de_passe']) :

                df=pd.read_sql_query(f'''SELECT DISTINCT nom_de_compte
                                         FROM authentification
                                         WHERE mail = "{mail}" ''', con)

                #Rajoute l'utilisateur a la session, récupère son nom
                df=pd.read_sql_query(f'''SELECT DISTINCT nom_de_compte
                                     FROM authentification
                                     WHERE mail = "{mail}"''', con)
                session['nom_de_compte'] = df['nom_de_compte'][0]

                #Recupere le niveau de sécurité de l'utilisateur
                df=pd.read_sql_query(f'''SELECT DISTINCT niveau_de_compte
                                     FROM authentification
                                     WHERE mail = "{mail}"''', con)
                #Session est un objet JSON, il n'accepte que les str et pas les
                #int donc on cast notre niveau de compte en str
                session['niveau_de_compte'] = str(df['niveau_de_compte'][0])

                return redirect("/connexion_success")
                #Creer le cookie qui au fond ne sert a rien dans l'instant
                #Pour transporter un cookie il est nécésaire de modifier la
                #reponse du serveur à la requête HTML, au lieu de simplement
                #render_template/redirect on cree alors une reponse et on y
                #Rajoute un cookie
                # reponse = make_response(redirect('/connexion_success'))
                # reponse.set_cookie('pseudo', df['nom_de_compte'][0])
                # return reponse

    return redirect("/connexion_fail")

@app.route('/connexion_success')
def connexion_success() :
    return render_template('message_connexion_success.html')

@app.route('/connexion_fail')
def connexion_fail() :
    return render_template('message_connexion_fail.html')


@app.route('/renseignement',methods=['GET'])
def renseignement() :
    """Nous récupérons les données que l’utilisateur rentre dans le formulaire :
    l’âge, la taille, le poids, le genre, s’il est sportif,
    ses allergies, ses objectifs."""
    return render_template("renseignement.html")

######################################################################
#------- Pour auto completion [liste_aliments.py] -------------------#
######################################################################


class SearchFormLegume(Form):
    autocomp = TextField('Entrez un légume', id='legume_autocomplete')
### pour viande
# class SearchFormViande(Form):
#     autocomp = TextField('Entrez un légume', id='legume_autocomplete')

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(new_liste_legumes), mimetype='application/json')


@app.route('/interactive', methods=['GET', 'POST'])
def index():
    form = SearchFormLegume(request.form)
    return render_template("interactive.html", form=form)


#### pour viande
# class SearchFormViande(Form):
#     autocomp = TextField('Entrez un légume', id='legume_autocomplete')



#A integrer
# new_liste_viandes
# new_liste_fromages
# new_liste_fruits
# new_liste_allergies
######################################################################
#----------------------- Fin autocomletion  -------------------------#
######################################################################


if __name__ == '__main__':
    app.run(debug=False)
