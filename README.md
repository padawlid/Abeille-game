BZZZ - Guerre des Abeilles
Projet SAÉ 1.01 - Implémentation d'un besoin client
IUT - Année 2025-2026

Description
BZZZ est un jeu de stratégie au tour par tour où 4 joueurs s'affrontent en contrôlant des colonies d'abeilles.
Le but est de récolter le maximum de nectar en explorant le plateau, en butinant des fleurs et en combattant les adversaires.

Auteurs


Date : Janvier 2025

-- Installation et lancement --

Prérequis

Python (installé sur les machines de l'IUT)
Tkinter (inclus par défaut avec Python)
Aucune installation supplémentaire requise

-- Lancement du jeu --
bashpython main.py
Le jeu se lance directement avec un menu de sélection du mode de jeu.

-- Lancement des tests --
bashpython test_model.py

 
-- Structure du projet --
BZZZ/
├── main.py              # Interface graphique et gestion des événements
├── model.py             # Logique du jeu (règles, plateau, abeilles)
├── ia.py                # Intelligence artificielle
├── test_model.py        # Tests unitaires
├── README.txt           # Ce fichier
├── regles_bzzz.pdf      # Règles officielles du jeu
├── sujet_BZZZ.pdf       # Sujet de la SAÉ
└── image/               # Dossier contenant les sprites
    ├── abeilles/        # Images des abeilles (par type, couleur, direction)
    ├── ruches/          # Images des ruches (par couleur)
    ├── fleur.png        # Image de fleur
    └── terre_seamless.png # Texture du sol

-- Règles du jeu --
Pour les règles complètes, consulter regles_bzzz.pdf.
Résumé :

4 joueurs s'affrontent sur un plateau 16x16
3 types d'abeilles :

Ouvrières : Capacité de nectar élevée (12), déplacement en ligne droite
Éclaireuses : Mobilité (déplacement en diagonale), capacité moyenne (3)
Bourdons : Force élevée (5), faible capacité (1)

4 phases par tour :

Ponte : Créer une abeille (coût : 5 nectars)
Mouvement : Déplacer ses abeilles
Butinage : Récolter du nectar sur les fleurs
Escarmouches : Combat automatique si abeilles ennemies adjacentes



Conditions de victoire

Timeout : Après 300 tours, le joueur avec le plus de nectar gagne
Blitzkrieg : Un joueur récolte plus de la moitié du nectar total
Épuisement : Plus de nectar disponible sur le plateau


-- Contrôles --
Phase Ponte

Cliquer sur les boutons "OUVRIERE", "ECLAIREUSE" ou "BOURDON" pour pondre
Cliquer sur "PASSER LA PHASE" pour passer à la phase suivante
Astuce : Vous pouvez programmer des pontes pour les tours suivants en cliquant pendant les autres phases (file d'attente)

Phase Mouvement

Cliquer sur une abeille pour la sélectionner (cercle blanc)
Cliquer sur une case pour déplacer :

Case adjacente → Déplacement immédiat
Case lointaine → Déplacement automatique sur plusieurs tours (prémove)


Les cases vertes indiquent les déplacements possibles
"PASSER LA PHASE" pour terminer (ou auto-skip si toutes les abeilles ont bougé)

Phase Butinage

Cliquer sur une abeille adjacente à une fleur pour butiner
Auto-skip si aucune abeille ne peut butiner
Le nectar est automatiquement déposé quand l'abeille rentre dans sa zone de ruche

Raccourcis automatiques

- Auto-skip des phases sans actions possibles
- Dépôt automatique du nectar en zone de ruche
- File de pontes pour programmer des abeilles à l'avance


-- Modes de jeu --
Modes Hot-Seat (joueurs locaux)

4 JOUEURS : Mode classique, 4 joueurs en local
3 JOUEURS : Ruche 4 désactivée
2 JOUEURS : Ruches 3 et 4 désactivées
1 JOUEUR : Seule la ruche 1 est active (entraînement)

Modes avec IA

3 JOUEURS + 1 IA : 3 humains vs 1 IA
2 JOUEURS + 2 IA : 2 humains vs 2 IA
1 JOUEUR + 3 IA : 1 humain vs 3 IA
4 IA (MODE SPECTATEUR) : Observer 4 IA s'affronter


-- Fonctionnalités implémentées --

Niveaux du modèle

- Niveau 1 : Déplacement, ponte, gestion du nectar
- Niveau 2 : Fleurs, butinage, escarmouches, fin de partie
- Niveau 3 : Mode 1 joueur contre 3 IA

Niveaux graphiques

- Niveau 1 : Affichage graphique complet
- Niveau 2 : Contrôles à la souris, infos en temps réel
- Niveau 3 : Déplacements automatiques (prémove)

Options supplémentaires

- File d'attente de pontes : Programmer des pontes futures
- Déplacements automatiques : Prémove pour trajets longs
- Auto-skip intelligent : Saute les phases vides
- Modes de jeu variés : 1 à 4 joueurs
- Interface graphique complète : Sprites, animations, couleurs

Tests unitaires

- 7 tests unitaires dans test_model.py
- Tests des fonctions critiques (ponte, déplacement, escarmouches)
- Tests des conditions de victoire


-- Intelligence Artificielle --
L'IA utilise un système de scoring pour prendre ses décisions :
Stratégie de ponte

Rush ouvrières en début de partie (collecte de nectar)
Ratio optimal : 50% ouvrières, 25% éclaireuses, 25% bourdons
Marge de sécurité : Garde toujours du nectar en réserve

Stratégie de mouvement

Abeilles avec nectar -> Retour à la ruche (priorité absolue)
Abeilles sans nectar -> Recherche de fleurs
Évite les zones dangereuses (beaucoup d'ennemis)

Stratégie de butinage

Butine avec toutes les abeilles qui ont une fleur accessible


-- Choix de conception --

Architecture

Séparation modèle/vue : model.py (logique) et main.py (affichage)
Pattern Tkinter classique : Fonction afficher_plateau() contient les fonctions locales
Variables nonlocal : Partage d'état entre fonctions imbriquées

Fonctionnalités ergonomiques

File de pontes : Évite d'attendre la phase de ponte
Déplacements automatiques : Trajets longs simplifiés
Auto-skip : Accélère le jeu en sautant les phases vides

Limitations connues

Fonction afficher_plateau() longue (~600 lignes) mais pattern classique de Tkinter
Pas de sauvegarde de partie
IA basique (pas de stratégie avancée)


-- Problèmes connus --
"L'abeille ne se déplace pas"
Vérifiez qu'elle n'a pas déjà bougé ce tour (a_bouge = True)
"Je ne peux pas pondre"

Vérifiez :

Avoir au moins 5 nectars
Case de ruche libre

"La phase ne passe pas automatiquement"
→ Vérifiez qu'il ne reste pas d'abeilles pouvant encore agir

-- Tests et validation -- 
Le jeu a été testé sur les scénarios suivants :

- Partie complète 4 joueurs
- Partie 1 joueur vs 3 IA
- Toutes les conditions de victoire (timeout, blitzkrieg, épuisement)
- Tous les types d'abeilles et leurs capacités
- Escarmouches avec différentes configurations
- Tests unitaires (7 fonctions critiques)


-- Développement --
Lancer les tests
bashpython test_model.py
Structure des tests

test_creer_plateau() : Création du plateau
test_dans_zone_ruche() : Zones de ruches
test_distance_valide() : Calcul de distance
test_tenter_ponte() : Ponte d'abeilles
test_tenter_deplacement() : Déplacements
test_calculer_force_effective() : Escarmouches
test_fin_de_partie() : Conditions de victoire


-- Ressources --

Règles officielles : regles_bzzz.pdf
Sujet de la SAÉ : sujet_BZZZ.pdf
Documentation Python Tkinter : Tutoriels Youtube, Outils d'assistance à la programmation(IA : ChatGPT) 

-- Remerciements --
Merci aux enseignants de l'IUT pour ce projet passionnant !

-- Notes techniques --
Constantes du jeu

NCASES = 16           # Taille du plateau
NECTAR_INITIAL = 10   # Nectar de départ
COUT_PONTE = 5        # Coût pour pondre
TIME_OUT = 300        # Nombre max de tours
TIME_KO = 5           # Tours KO après escarmouche ratée
Capacités des abeilles
pythonCAPACITE_NECTAR = {
    "bourdon": 1,
    "eclaireuse": 3,
    "ouvriere": 12
}

FORCE = {
    "eclaireuse": 1,
    "ouvriere": 1,
    "bourdon": 5
}

Bon jeu !
