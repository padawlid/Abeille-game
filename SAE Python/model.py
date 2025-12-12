#modèle du jeu

NCASES = 16 #taille du plateau
NECTAR_INITIAL = 10 #nectar de départ
MAX_NECTAR = 45 #max nectar par fleur
COUT_PONTE = 5 #coût d'une abeille
TIME_OUT = 300 #nombre max de tours
TIME_KO = 5 #nombre de tours qu'une abeille KO reste KO


#Niveau 1 
def creer_plateau():
    """
    crée un plateau vide : chaque case doit être une liste vide pour contenir plusieurs éléments
    avec les paramètres pour savoir les positions plus tard.
    On veut un truc comme ça :
    [0,0] [0,1] [0,2] ... [0,15]
    [1,0] [1,1] [1,2] ... [1,15]
    ...
    [15,0] ...            [15,15]

    On va d'ailleurs aussi stocker les ruches et fleurs ici directement
    """
    plateau = []
    for i in range(NCASES):
        ligne = []
        for j in range(NCASES):
            ligne.append([])  # chaque case = liste vide
        plateau.append(ligne)


    
    
    return plateau

def creer_ruche(plateau):
    ruche0 = {
        "type": "ruche",
        "id": "ruche0",
        "nectar": 0,
        "abeilles": []
    }
    ruche1 = {
        "type": "ruche",
        "id": "ruche1",
        "nectar": 0,
        "abeilles": []
    }
    ruche2 = {
        "type": "ruche",
        "id": "ruche2",
        "nectar": 0,
        "abeilles": []
    }
    ruche3 = {
        "type": "ruche",
        "id": "ruche3",
        "nectar": 0,
        "abeilles": []
    }
    # Placer les ruches dans les coins
    plateau[0][0] = ruche0
    plateau[0][NCASES-1] = ruche1
    plateau[NCASES-1][0] = ruche2
    plateau[NCASES-1][NCASES-1] = ruche3

    ruches = [ruche0, ruche1, ruche2, ruche3]
    return ruches

    
def creer_fleurs():
    """
    On va crée des fleurs mais pas dans le plateau.
    On determinera les positions aussi
    """
    fleurs = []

    centre = NCASES // 2
    
    positions = [
        (centre-1, centre-1),
        (centre-1, centre),
        (centre, centre-1),
        (centre, centre),
    ]

    i = 0 #ajout d'un compteur 
    for pos in positions:

        x = pos[0]
        y = pos[1]
        #on va crée les stats de la fleur
        fleurs.append({
            "id": f"fleur{i}",  
            "nectar": 10,
            "position": (x, y)
        })

        i = i + 1  # on augmente le compteur

    return fleurs

def placer_fleurs(plateau, fleurs):
    for fleur in fleurs:
        x, y = fleur["position"]
        plateau[x][y].append(fleur)

# def creer_abeille(type_abeille, position):
#     """
#     Crée une abeille avec son type, position, son état et son nectar (0)
#     """
#     return {
#         "type": type_abeille, 
#         "position": position,
#         "nectar": 0,
#         "etat": "OK"
#     }

# def placer_abeille(plateau, abeille):
#     x, y = abeille["position"]
#     if plateau[x][y] is None:
#         plateau[x][y] = [abeille]
#     else:
#         plateau[x][y].append(abeille)


# def gestion_totale_nectar(ruches, index_ruche, action, abeille=None):
#     """
#     Gère le nectar pour une ruche
#     action = "ponte" ou "rapporte_nectar"
#     """
#     ruche = ruches[index_ruche]
#     if action == "ponte" and abeille:
#         if ruche["nectar"] >= COUT_PONTE:
#             ruche["nectar"] -= COUT_PONTE
#             ruche["abeilles"].append(abeille)
#             print(f"Abeille {abeille['type']} ajoutée à la ruche {index_ruche}")
#         else:
#             print("Pas assez de nectar pour pondre !")

# def deplacer_abeille(plateau, abeille, nouvelle_position):
#     x_old, y_old = abeille["position"]
#     plateau[x_old][y_old].remove(abeille)  #On enlève de l'ancienne case

#     x_new, y_new = nouvelle_position
#     abeille["position"] = (x_new, y_new)   #On met à jour sa position

#     if plateau[x_new][y_new] is None: #Ajout
#         plateau[x_new][y_new] = [abeille]
#     else:
#         plateau[x_new][y_new].append(abeille)

def startgame(): 
    """
    creer_plateau() → crée le plateau vide (des listes vides)

    creer_ruches() → crée les dicts des ruches

    creer_fleurs() → crée les dicts des fleurs

    placer_fleurs() → place les fleurs dans le plateau

    creer_abeille() → crée un dict abeille

    placer_abeille() → met les abeilles sur le plateau

    gestion_nectar() → gère les ruches

    startgame() → assemble tout
    """
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs()
    placer_fleurs(plateau,fleurs)


startgame() #Lancement du jeu