"""
RECOMMANDATION ALIMENTAIRES A PARTIR DES VALEURS NUTRITIONNELLES

A partir des contenus des repas renseignés par un utilisateur, et des conseils
des nutritionnistes, on se propose de donner des recommandations de menus pour
rester au maximum de sa forme. L'algorithme se sert des informations
renseignées par des personnes similaires susceptibles d'avoir des habitudes
alimentaires les meilleures, ainsi que des sites web donnant des conseils et
des recettes. Chaque utilisateur peut ainsi apprendre de lui-même et des
autres.

1 - LES DONNEES UTILISEES
La source de données la plus détaillée permettant d'accéder aux
caractéristiques des aliments disponibles sur le marché est Open Food Fact.
Le site donne accès à fichier qui donne accès en juin 2020 à 1,3 millions
d'aliments caractérisés par 180 champs. Schématiquement les informations
données sont

id , nom_produit   , proteine_100g,  glucide_100g, lipide_100g
1  , Céréal        , 20           ,  50          , 30
2
3

Les types d'informations accessibles sont les suivants:
    - l'identification du produit, lieu de fabrication...
    - compositions (glucide, lipide, protéine, minnéraux, vitamines...)

Les analyses nutritionelles seront menées

@author: Joseph, Léa, Lee Roy

# TODO :
1°) (Léa) Créer un structure simplifiée // fabrication
1°) (Léa) Etoffer les exemples de données (à la main) // fait
1°) (Léa) Etoffer les exemples de données
    (avec un générateur aléatoire) // fait (+Joseph)

2°) Créer les fonction de calcul de base:
2-a) (Joseph) valeur_nutritionnelle et bilan_nutritionnel // fait
2-b) (Lee Roy) carences // fait

3°) Faire les graphiques d'analyse // fait
4°) Connecter les fonctions à la base de données
"""

### Import

import numpy as np
import datetime as date
import random as rd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1°) STRUCTURE DE DONNEES SIMPLIFIEE
# REMARQUE pour Léa :
# a) Pour des données structurées complexes, il faut indenter le code
# comme ci-dessous pour une plus grande clareté // fait
# b) Respecter les règles de mise en forme PEP8 // fait je crois
# voir: https://www.python.org/dev/peps/pep-0008/
# en particulier:
# i) pas d'espace devant : dans les dictionnaires
# ii) un espace après les vigules dans les fonctions
# iii) deux lignes vides avant chaque fonction
# Pour être à l'aise avec ça installer Python Autopep8 dans Atom // marche pas
# Faire un point sur pep8 à tous le groupe Jeudi à la réunion du soir // fait

### Structure de données

date_1, date_2 = date.datetime(2020, 1, 1), date.datetime(2020, 12, 31)
utilisateurs = {
    "Lea": {
        "genre": "femme",
        "repas": {
            date_1: [
                {"nom": "carotte", "quantite": 100},
                {"nom": "petit pois", "quantite": 21}],
            date_2: [
                {"nom": "carotte", "quantite": 100},
                {"nom": "petit pois", "quantite": 21}]}},
    "Leeroy": {
        "genre": "homme",
        "repas": {
            date_1: [
                {"nom": "carotte", "quantite": 100},
                {"nom": "petit pois", "quantite": 21}],
            date_2: [
                {"nom": "carotte", "quantite": 100},
                {"nom": "petit pois", "quantite": 21}]}},
    "Joseph": {
        "genre": "homme",
        "repas": {
            date_1: [
                {"nom": "carotte", "quantite": 100},
                {"nom": "petit pois", "quantite": 21}],
            date_2: [
                {"nom": "carotte", "quantite": 100},
                {"nom": "petit pois", "quantite": 21}]}}
               }

# faire attention aux /sous-catégories de nutriments
# "énergie" exprimée en kcal
#conseils_nutritionnels["homme ou femme"]["tranche d'age"]["nutriment"]
conseils_nutritionnels = {
    "homme": {
        "20-30ans": {
            "lipides": 90,
            "glucides": 260,
            "fibres": 27,
            "proteines": 50,
            "sel": 6,
            "sucres": 90,
            "energie": 2000}},
    "femme": {
        "20-30ans": {
            "lipides": 90,
            "glucides": 260,
            "fibres": 27,
            "proteines": 50,
            "sel": 6,
            "sucres": 90,
            "energie": 2000}}
            }

# valeurs nutri pour 100g
valeur_nutritionnelle = {
    "carotte": {"glucides": 6.45, "fibres": 2.7, "sucres": 5.42},
    "pomme de terre": {"glucides": 16.7, "fibres": 1.8, "sucres": 0.86},
    "jambon": {"glucides": 1.3, "fibres": 0, "sucres": 1.3},
    "semoule": {"glucides": 72.83, "fibres": 3.9, "sucres": 0},
    "yaourt": {"glucides": 6.68, "fibres": 0, "sucres": 4.66},
    "escalope": {"glucides": 0, "fibres": 0, "sucres": 0},
    "haricots verts": {"glucides": 3.63, "fibres": 4, "sucres": 1},
    "tomates": {"glucides": 2.26, "fibres": 1.2, "sucres": 2.25},
    "salade": {"glucides": 1.37, "fibres": 1.3, "sucres": 1.7},
    "lardons": {"glucides": 0.6, "fibres": 0, "sucres": 0.46},
    "pâtes": {"glucides": 29.7, "fibres": 2.28, "sucres": 5.42},
    "petit pois": {"glucides": 4.7, "fibres": 5.8, "sucres": 0.47},
    "concombre": {"glucides": 2.04, "fibres": 0.6, "sucres": 1.34},
    "abricot": {"glucides": 7.14, "fibres": 1.8, "sucres": 6.57},
    "quiche": {"glucides": 22.2, "fibres": 0.90, "sucres": 1.7},
    "maïs": {"glucides": 15.41, "fibres": 1.7, "sucres": 4.54},
    "pizza": {"glucides": 27.7, "fibres": 2.36, "sucres": 2.6},
    "banane": {"glucides": 19.6, "fibres": 1.9, "sucres": 14.8},
    "pomme": {"glucides": 11.6, "fibres": 1.4, "sucres": 9.35}}

### Modélisation Orienté Objet

class utilisateur():
    """ Nous cherchons à modélisé un utilisateur, cet utilisateur cherche à
    obtenir des informations nutrionel adapté à son physique et ses désires
    pour cela il est nécéssaire de connaître une série d'information relative
    au corp de cette utilisateur, un historique de ses repas (pour conseillé
    des alternatives) une série de tag lié au régime alimentaire (végétarien,
    sans sel etc...) et un ou plusieurs objectif (devenir végétarien,
    gagné/perdre du poids, favorisé le gain de muscle)
    """
    def __init__(self, nom, genre, age, poids, taille):
        self.nom = nom
        self.genre = genre
        self.age = age
        self.poids = poids
        self.taille = taille
        # Dictionnaires {date : ingredient/valeur}
        # A terme devrais être un dictionaire de dataframes
        self.repas = {}
        # Tag servant à éxclure certain type de nourritures des suggestions
        self.tag_regime = []
        # Tag servant à modifié le profil nutrionnel de base pour repondre
        # au désires de l'utilisateur
        self.tag_objectif = []
        # Structure qui contient un profil nutrionel personalisé résultant de
        # la modification de profil type par les tag_regime, tag_objectifs
        self.profil_personnel = {}

    def ajoute_repas(self, date, repas):
        """Un repas est une date ainsi qu'un ou plusieurs ingredient(s) ou
        produit(s), fonction d'exemple il serais possible de faire
        utilisateur.repas[date] =
        """
        self.repas[date] = repas

### Fonction de génération de données

def generateur_repas(nom, date, nbr_ingredients):
    """ La fonction génère 4 repas pour l'utilisateur à la date passée en
    paramètre, à partir d'une liste d'aliments prédéfinis associés
    à une quantité générée aléatoirement entre 30g et 120g.
    Appeler la fonction et générer 4 repas pour Joseph au 2020/06/10 :
    generateur_repas(utilisateurs["Joseph"], date.datetime(2020, 6, 10))
    """

    aliments = [
        "carotte", "petit pois", "pomme de terre", "jambon", "semoule",
        "yaourt", "escalope", "haricots verts", "tomates", "salade",
        "lardons", "pâtes", "concombre", "maïs", "pizza", "banane",
        "pomme", "abricot", "quiche"]
    for x in range(0, nbr_ingredients):
        aliment = np.random.choice(aliments)
        quantite = int(np.random.randint(30, 120, 1))
        nom["repas"][date] += [{"nom": aliment, "quantite": quantite}]


##Joseph 12
def date_aleatoire(date_debut, date_fin):
    """Génère une date aléatoire entre celles passé en paramètre, cette date
    est obtenu par un timedelta issu du nombre de jours entre elles
    """
    delta_date = date_fin - date_debut
    jours_entre_dates = delta_date.days
    nombre_de_jours = rd.randrange(jours_entre_dates)
    return (date_debut + date.timedelta(days=nombre_de_jours))


def generateur_historique_repas(utilisateurs, date_debut, date_fin,
                                nbr_date = 60,
                                nbr_ingredients = 4):
    """Fonction qui génère des dates de repas ainsi que leurs contenu en
    aliments sur une période défini en paramètre pour tout les utilisteurs
    dans la structure utilisteurs passé en paramètre
    """
    for utilisateur in utilisateurs :
        for i in range(nbr_date) :
            #genere la clef date
            date = date_aleatoire(date_debut, date_fin)
            #Prepare la liste pour recevoir les ingredients
            utilisateurs[utilisateur]["repas"][date] = []
            #rempli la liste de nbr_ingredients généré aléatoirement
            generateur_repas(utilisateurs[utilisateur], date, nbr_ingredients)
##Joseph 12

### Fonction de calcul d'information

def valeur_repas(repas, valeur_aliments):
    """Fonction qui ressort la valeur nutritionel d'un repas, un repas est une
    liste d'aliments, exemple basé sur la structure :
        utilisateurs["lea"]["repas"][date]
    valeur_aliments est un dictionnaire au format :
        {nom_aliments : valeur nutri}
    Pour appeler la fonction :
    valeur_repas(utilisateurs["Lea"]["repas"][date_1], valeur_nutritionnelle)
    """
    valeur_repas = {"glucides": 0, "fibres": 0, "sucres": 0}

    for aliment in repas:
        nom = aliment["nom"]
        if nom in valeur_aliments:
            for nutriment in valeur_aliments[nom]:
                val_gramme = valeur_aliments[nom][nutriment]/100
                valeur_repas[nutriment] += (val_gramme * aliment["quantite"])
    return valeur_repas


def bilan_nutritionnel(personne, valeur_nutri, date_debut, date_fin):
    """Fonction qui ressort la valeur nutritionnel total des repas entre
    deux dates.
    """
    for repas in utilisateurs[personne]["repas"]:
        if repas>=date_debut and repas<=date_fin:
            bilan = {}
            bilan = valeur_repas(repas, valeur_nutri, bilan)
    return bilan


# Lee-Roy Debut 11/06/2020
def valeur_nutrition_sur_nbJours(dico_nutrition, nbjour):
    """ Transforme les valeurs du dico_nutrition sur une echelle de temps,
        ici en nombre de jour
                :param dico_nutrition : dictionnaire de nutritione
                :param nbjour : nombre de jour
            Exemple:
                >>> valeur_nutrition_sur_nbJours(conseils_nutritionnels,
                                                    6)
    """
    liste_nutriment = [
        'lipides', 'glucides', 'fibres', 'proteines', 'sel',
        'sucres', "energie"]

    for ingredient in dico_nutrition:
        if ingredient in liste_nutriment:
            dico_nutrition[ingredient] *= nbjour
    dico_nutri_nb_j = dico_nutrition
    return dico_nutri_nb_j


def carences(personne, date_debut, date_fin):
    """ Affiche les carences selon l'alimentation sur 1 semaine (6 jour)
    car le dimanche c'est le cheat meal, la fonction prends une personne
    en parametre (donc le nom, et les repas, la date du debut et la date de
    fin)
            :param personne : personne dont on cherche la carence
            :param date_debut : début de la recherche a partir
                                de la date selectionnée
            :param date_fin : fin de la recherche

        Exemple:
            >>> carances("Lea", date.datetime(2020, 6, 10),
                        date.datetime(2020, 6, 11))
    """
    valeur_repas = {'glucides': 0, 'fibres': 0, 'sucres': 0}
    repas = utilisateurs[personne]['repas']

    for date_repas in repas:
        if date_repas >= date_debut and date_repas <= date_fin:
            for aliment in repas[date_repas]:
                nom = aliment["nom"]
                quantite = aliment["quantite"]
                if nom in valeur_nutritionnelle:
                    for nutriment in valeur_nutritionnelle[nom]:
                        nutri = valeur_nutritionnelle[nom][nutriment]
                        valeur_repas[nutriment] += nutri * quantite/100

    sexe = utilisateurs[personne]["genre"]
    date_delta = date_fin - date_debut
    nb_jour = date_delta.days
    dico_nb_jour = valeur_nutrition_sur_nbJours(conseils_nutritionnels[sexe]
                                                ["20-30ans"], nb_jour)

    dico_tmp = dico_nb_jour.copy()
    # Je vais regarder si j'ai mes nutriments correspondant à mon dico
    # sur x jour
    for nutriment in dico_tmp:
        if nutriment not in list(valeur_repas):
            # Si non, je les supprimes de mon dictionnaire
            del dico_nb_jour[nutriment]

    for nutriments, valeurs in valeur_repas.items():
        if nutriments in dico_nb_jour:
            if valeurs < dico_nb_jour[nutriments]:
                print("Vous avez une carence en ", nutriments)
    return valeur_repas, dico_nb_jour
# Lee-Roy fin 12/06/2020

### Production de Graphs


def rendu_graphique(personne, mode, date_debut=None, date_fin=None, date=None):
    """Fonction de rendu graphique, cette fonction a pour but de produire
    un groupe de graphiques représentant une information sensée liée à
    la consommation alimentaire de l'utilisateur il prend comme paramètre une
    personne, un mode, et une ou plusieurs dates en fonction du mode choisi.

    mode == "repas" : ce mode demande une seule date et fourni le bilan
    nutrionnel du repas lié à cette date, il renvoie deux graphiques un pour
    le repas cumulé et un autre pour les aliments.

    mode == "bilan" :  ce mode demande une date de début et une date de fin,
    il permet de visualiser la consommation en nutriments à travers le temps
    permettant d'observer des carences ou excès sur une durée définie.

    mode == "carence" : ce mode demande une date de début et de fin, il permet
    de visualiser les carences en nutriments en fonction de la personne cette
    visualisation se fait à travers un graph bar superposant la consommation
    sur les carences.


            :param personne : personne qui possède un historique de repas
            :param
            :param date_debut : date de début de l'observation
            :param date_fin : date de fin de l'observation
    """
    if mode == "repas": #Léa
        """Graph Bar des nutriments cumulés d'un repas passé en paramètre
        avec MATPLOTLIB
        """
        personne = utilisateurs[personne]
        donnee_graph = valeur_repas(personne["repas"][date],
                                    valeur_nutritionnelle)
        legende = list(donnee_graph.keys())
        x = np.arange(len(donnee_graph))
        y = donnee_graph.values()

        fig, ax = plt.subplots()
        plt.bar(x, y)
        plt.xticks(x, labels=legende)
        plt.title('Valeurs nutritionnelles')
        plt.xlabel('Nutriments')
        plt.ylabel('Quantité en grammes')
        plt.savefig("static\images\graph_repas.png", bbox_inches='tight')
        plt.show()

        """Graph bar (subplots) des nutriments par aliment d'un repas passé
        en paramètre avec SEABORN
        """
        donnees = personne["repas"][date_1]
        # reprise valeur_repas pour calculer et récupérer les apports
        # nutritionnels d'un repas en séparant ses aliments
        valeur_nutri = {}
        for produit in donnees:
            nom = produit["nom"]
            if nom in valeur_nutritionnelle:
                valeur_produit = {"glucides": 0, "fibres": 0, "sucres": 0}
                for nutriment in valeur_nutritionnelle[nom]:
                    val_gramme = valeur_nutritionnelle[nom][nutriment]/100
                    valeur_produit[nutriment] = (val_gramme *
                                                 produit["quantite"])
                    valeur_nutri[nom] = valeur_produit
                print("DICO DE DONNÉES PRODUITS : ", valeur_nutri)

        # transfert dico vers dataframe
        data = pd.DataFrame.from_dict(valeur_nutri, orient = 'index')
        # axes du graphique générés dynamiquement pour les subplots
        axes = {}
        i = 1
        for aliment in valeur_nutri:
            axes[aliment] = "ax" + str(i)
            i += 1
        axs = list(axes.values())

        sns.set(style="white", context="talk")
        f, axs = plt.subplots(len(axs), 1, figsize=(10, 10), sharex = True)
        # tracé du graphique
        i = 0
        for element in data.index:
            x = data.columns
            y = data.iloc[i]
            sns.barplot(x=x, y=y, palette="rocket", ax=axs[i])
            i += 1

        plt.title('Valeurs nutritionnelles par aliment')
        plt.savefig("static\images\graph_ingredient.png", bbox_inches='tight')
        plt.show()

    if mode == "bilan":  # Joseph //fait 12/06
        """Graph qui montre la consomation de chaque nutriments par jour
        pour la durée passé en paramètre
        """
        personne = utilisateurs[personne]


        def graph_bilan(repas, date_debut,date_fin) :
            """fonction qui crée un graph des nutriments par jours entre deux date,
            une structure intermédiare est crée sous forme de dataframe avec pour
            index les dates et pour colonnes nutriments
            """
            dates = []
            bilans = []
            for date_repas in repas :
                if date_repas >= date_debut and date_repas <= date_fin :
                    dates += [date_repas]
                    bilans += [valeur_repas(repas[date_repas],
                                            valeur_nutritionnelle)]

            df = pd.DataFrame(bilans, index=dates)
            sns.lineplot(data=df, palette="tab10", linewidth=2.5)
            plt.savefig("static\images\graph_bilan.png", bbox_inches='tight')
            plt.show()

        graph_bilan(personne["repas"], date_debut, date_fin)

    # Debut 12/06
    if mode == "carence":  # Lee-Roy
            """Graph double bar surperposition d'un nutriment sur
            son taux espéré avec carence
            """

            dico_mes_repas, dico_conseil = carences(personne, date_debut,
                                                    date_fin)

            sns.set(style="whitegrid")
            f, ax = plt.subplots(figsize = (6, 15))
            df_valeur_conseille = pd.DataFrame.from_dict(dico_conseil,
                                                        orient = 'index',
                                                        columns = ["values"])
            df_valeur_repas = pd.DataFrame.from_dict(dico_mes_repas,
                                                    orient = 'index',
                                                    columns = ["values"])
            x1 = list(df_valeur_conseille.index)
            y1 = list(df_valeur_conseille["values"])
            sns.set_color_codes("pastel")
            f = sns.barplot(x = x1, y = y1, data = df_valeur_conseille,
                            label = "conseillée", color = "b")
            f.set(yscale = "log")
            f.set_xticklabels(f.get_xticklabels(), rotation = 90)
            sns.set_color_codes("muted")
            x2 = list(df_valeur_repas.index)
            y2 = list(df_valeur_repas["values"])
            ax = sns.barplot(x = x2, y = y2, data = df_valeur_conseille,
                            label = "actuel", color = "b")
            ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
            ax.legend(ncol = 2, loc = "upper right", frameon = True)
            ax.set(xlabel = "nutriments", ylabel = "valeurs")
            sns.despine(left = True, bottom = True)
            plt.title('Carence nutrionnelle')
            plt.savefig("static\images\graph_carence.png", bbox_inches='tight')
            plt.show()

    # Fin
if __name__ == "__main__":
  #appel la fonction de generation de données aléatoire
  generateur_historique_repas(utilisateurs,date_1,date_2)


  #Chaque appel de fonction crée son propre graphique
  rendu_graphique("Lea", "repas", date=date_1)
  rendu_graphique("Lea", "bilan", date_debut = date_1, date_fin = date_2)
  rendu_graphique("Lea", "carence",
                  date_debut = date.datetime(2020,1,1),
                  date_fin = date.datetime(2020,6,7))




