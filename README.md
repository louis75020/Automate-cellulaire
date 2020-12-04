# Automate-cellulaire - Louis LESUEUR
Projet de M2 création d'un automate cellulaire

## Lancer le programme :

Le module cellular_automaton contient un main. Vous pouvez le lancer à partir d'une console python ou avec la commande python3 cellular_automaton.py

Vous pouvez lancer le programme avec des arguments customisés à partir de cellular_automaton_manager avec la commande python3 cellular_automaton_manager.py path_vers_la_situation_initiale path_vers_la_matrice_de_transition path_vers_le_fichier_parametres_optionnels

Des fichiers d'INPUT sont proposés (voir section fichiers de tests); vous pouvez les utiliser ou vous en servir comme templates pour vos tests.

Leur structure est un peu plus détaillée dans la doc. dernière section.

### Requiert

Python 3 ou supérieur.

numpy

pandas

matplotlib

random

logging

pylab

sys

### Fichiers de tests

Configuration 1 : projet (sans expansion de l'univers, avec toutes les directions de transition possibles, étape par étape)

initial_statecg1; transition_matrix_cg1; params1.txt

Configuration 2 : Game of life-like (avec expansion de l'univers, toutes les directions de transition, plusieurs étapes à la fois)

initial_statecg2; transition_matrix_cg2; params2.txt

## Documentation

Au format html :

cellular_automaton_tests.html

Au format python :

cellular_automaton_tests.ipynb

## Programme

Module principal : tinder_manager, cellular_automaton_runner, cellular_automaton_plotter, cellular_automaton

Module secondaire : cellular_automaton_manager

Documentation au format .py : cellular_automaton_tests
