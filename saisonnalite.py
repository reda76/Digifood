# -*- coding: utf-8 -*-                                                                                                               -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 22:27:16 2020

@author: sébastien lehoux
ctrl+N  Nouveau fichier
ctrl+S  Sauver le fichier
ctrl+   Re-démarrer le noyau

Tab     Indenter
Maj+Tab Désindenter

Titre: des fruits et des légumes de saison
aide : 
déclaration: import saisonnalité

Description: ici j'ai constitué 2 dictionnaires "fruits" "légumes"
ainsi que leur période de saisonnalité pour les affichés dans une
page html




"""
from datetime import date

### variable de récupération de la date du jour
today = date.today()
# today = date(2020, 12, 23)

### Variable de récupération du mois
#today.year
mois = today.month
#today.day

### Déclaration des clés d'un dictionnaire de saisons
saisons = {'hiver':[],
          'printemps':[],
          'été':[],
          'automne':[]
          }

# saisons['hiver']=['janvier','février','mars']
# saisons['printemps']=['avril','mai','juin']
# saisons['été']=['juillet','aout','septembre']
# saisons['automne']=['octobre','novembre','decembre']

### Déclaration des valeurs du dictionnaire de saisons
saisons['printemps']=[date(2020, 3, 20), date(2020, 6, 19)]
saisons['été']=[date(2020, 6, 20), date(2020, 9, 21)]
saisons['automne']=[date(2020, 9, 22), date(2020, 12, 20)]
saisons['hiver']=[date(2020, 12, 21), date(2021, 3, 19)]

# saisons['hiver']=[1, 2, 3]
# saisons['printemps']=[4, 5, 6]
# saisons['été']=[7, 8, 9]
# saisons['automne']=[10, 11, 12]

### Boucle de définition de la saison actuelle pour la variable saison
saison = {}

for k, v in saisons.items():
    if today >= v[0] and today <= v[1]:
        print(k)
        saison.update({k: v})

# for k, val in saisons.items():
#     # print(val)
#     if mois in val:
#         print(k)
#         saison.update({k: v})

### Déclaration d'un dictionnaire de fruits et leur saisonnalité
liste_fruits = {
    'abricot': [6, 7, 8],
    'ananas': [1],
    'avocat': [1, 2, 3, 4],
    'cassis': [6, 7, 8],
    'cerise': [6, 7],
    'chataigne': [10, 11],
    'citron': [1, 2, 11, 12],
    'coing': [9, 10],
    'clémentine': [1, 2, 11, 12],
    'figue':[7, 8, 9, 10],
    'fraise': [5, 6, 7],
    'framboise': [6, 7, 8],
    'grenade': [1, 2, 11, 12],
    'groseille':[6, 7, 8],
    'kaki': [1, 10, 11, 12],
    'kiwi': [1, 2, 3, 11, 12],
    'mandarine': [1, 2, 11, 12],
    'mangue': [1, 2, 3, 4, 5, 11, 12],
    'melon': [6, 7, 8, 9],
    'mirabelle': [8, 9],
    'mure': [8, 9],
    'myrtille': [7, 8, 9],
    'nectarine': [7, 8],
    'noisette': [9, 10, 11],
    'noix': [9, 10],
    'orange': [1, 2, 3, 12],
    'pamplemousse': [4, 5, 6],
    'pastèque': [6, 7, 8],
    'pêche': [6, 7, 8, 9],
    'poire': [1, 2, 3, 8, 9, 10, 11, 12],
    'prune': [7, 8, 9],
    'pomme': [1, 2, 3, 4, 8, 9, 10, 11, 12],
    'quetsche': [8, 9, 10],
    'raisin': [9, 10],
    'reine claude': [9],
    'rhubarbe': [4, 5, 6]}

### Boucle de définition de sélection des fruits de saison
select_fruits = {}
for k, val in liste_fruits.items():
    # print(val)
    if mois in val:
        print(k)
        select_fruits.update({k: val})

### Déclaration d'un dictionnaire de légumes et leur saisonnalité
liste_legumes = {
    'ail': [7, 8, 9, 10, 11, 12],
    'artichaut': [5, 6, 7, 8, 9],
    'asperge': [4, 5, 6, 7],
    'aubergine': [6, 7, 8, 9],
    'betterave': [1, 2, 3, 10, 11, 12],
    'blette': [6, 7, 8, 9, 10],
    'brocoli': [9, 10, 11],
    'carotte': [1, 2, 3, 9, 10, 11, 12],
    'celeri': [1, 2, 3, 10, 11, 12],
    'champignon de paris': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'chou': [1, 2, 3, 10, 11, 12],
    'chou de bruxelles': [1, 2, 3, 10, 11, 12],
    'chou-fleur': [1, 2, 3, 9, 10, 11, 12],
    'concombre': [5, 6, 7, 8, 9, 10],
    'courge': [1, 9, 10, 11, 12],
    'courgette': [5, 6, 7, 8, 9, 10],
    'cresson': [1, 2, 3, 4, 5, 9, 10, 11, 12],
    'echalote': [10, 11, 12],
    'endive': [1, 2, 3, 4, 10, 11, 12],
    'epinard': [1, 2, 3, 4, 5, 9, 10, 11, 12],
    'fenouil': [4, 6, 7, 8, 9, 10, 11],
    'haricot vert': [6, 7, 8, 9, 10],
    'laitue': [5, 6, 7, 8, 9],
    'mache': [1, 2, 10, 11, 12],
    'mais': [7, 8, 9],
    'navet': [1, 2, 3, 4, 5, 10, 11, 12],
    'oignon': [1, 2, 3, 4, 9, 10, 11, 12],
    'panais': [1, 2, 3, 10, 11, 12],
    'petit pois': [5, 6, 7],
    'poireau': [1, 2, 3, 4, 9, 10, 11, 12],
    'poivron': [6, 7, 8, 9],
    'potiron': [1, 9, 10, 11, 12],
    'radis': [3, 4, 5, 6],
    'salsifis': [1,2, 11, 12],
    'tomate': [6, 7, 8, 9],
    'topinambour': [1, 2, 11, 12]}

### Boucle de définition de sélection des légumes de saison
select_legumes = {}
for k, val in liste_legumes.items():
    # print(val)
    if mois in val:
        print(k)
        select_legumes.update({k: val})

