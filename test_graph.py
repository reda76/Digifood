# Peggy 16/06/2020 DEBUT

# INTEGRATION DES GRAPHIQUES DE RECOMMANDATIONS ALIMENTAIRES SUR LE SITE WEB

# Librairies externes
from flask import Flask , render_template, redirect, url_for, flash, session, request
import numpy as np
import datetime as date
import random as rd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Librairies internes au projet
from graphiques import generateur_historique_repas, rendu_graphique, generateur_repas, carences
from graphiques import date_aleatoire, valeur_repas, bilan_nutritionnel, valeur_nutrition_sur_nbJours


#Declaration des constantes
mode = ['repas','bilan', 'carence']
date_1, date_2 = date.datetime(2020, 1, 1), date.datetime(2020, 12, 31)
date_debut = date.datetime(2020,1,1)
date_fin = date.datetime(2020,6,7)
date=date_1
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

# Initialisation de l'application web avec Flask
app=Flask(__name__)

generateur_historique_repas(utilisateurs,date_1,date_2)

@app.route('/')
def info():
    return render_template("graph_aliments.html")

@app.route('/graph_aliments', methods=['POST'])
def graph():

    mode = request.form['mode']

    # les if déterminent le type de graphique souhaité à la page précédente.
    # selon le type de graphe choisi
    if mode == "repas":
        rendu_graphique("Lea", "repas", date=date_1)
        rendu_graphique(utilisateurs, mode, date_debut, date_fin, date)

    if mode == "bilan":
        rendu_graphique(utilisateurs, mode, date_debut, date_fin, date)

    if mode == "carence":
        rendu_graphique(utilisateurs, mode, date_debut,date_fin, date)

    return render_template("graph_aliments.html")


app.run(debug=False)

# Peggy 16/06/2020 FIN