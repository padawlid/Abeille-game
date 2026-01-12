# MODELE.PY 
"""
Module contenant toute la logique du jeu BZZZ.

Ce fichier gère le modèle de données et les règles du jeu :
- Création du plateau et des éléments (ruches, fleurs, abeilles)
- Gestion des phases de jeu (ponte, mouvement, butinage, escarmouche)
- Conditions de victoire et fin de partie

Aucun code graphique ici, uniquement de la logique pure !
"""
import random

NCASES = 16 # taille plateau
NECTAR_INITIAL = 10 #au lancement
MAX_NECTAR = 45 #de UNE fleur
COUT_PONTE = 5
TIME_OUT = 300 
TIME_KO = 5
NFLEURS = 4 #nb de fleur placé
CAPACITE_NECTAR = { #nombre de fleur pouvant être stocké dans chaque type d'abeille
    "bourdon": 1,
    "eclaireuse": 3,
    "ouvriere": 12
}
FORCE = {
    "eclaireuse":1,
    "ouvriere":1,
    "bourdon":5
}

#----Création des paramètres de bases----
def creer_plateau():
    """
    Crée un plateau de jeu vide de taille NCASES x NCASES (16x16).
    
    Returns:
        list: Plateau de jeu, liste 2D où chaque case est une liste vide.
              Structure : plateau[ligne][colonne] = []
    
    Exemple:
        >>> plateau = creer_plateau()
        >>> len(plateau)  # 16 lignes
        16
        >>> len(plateau[0])  # 16 colonnes par ligne
        16
        >>> plateau[0][0]  # Case vide au départ
        []
    """
    plateau = []
    for _ in range(NCASES):
        ligne = []
        for _ in range(NCASES):
            ligne.append([])
        plateau.append(ligne)
    return plateau

def creer_ruche(plateau):
    """
    Crée les 4 ruches et les place dans les coins du plateau.
    
    Chaque ruche démarre avec NECTAR_INITIAL points de nectar (10) et 
    aucune abeille. Les ruches sont automatiquement ajoutées au plateau.
    
    Args:
        plateau (list): Plateau de jeu 16x16 créé par creer_plateau()
    
    Returns:
        list: Liste des 4 ruches [ruche0, ruche1, ruche2, ruche3]
    
    Positions des ruches:
        - Ruche 0 : coin haut-gauche (0, 0)     - Joueur bleu
        - Ruche 1 : coin haut-droite (0, 15)    - Joueur rouge
        - Ruche 2 : coin bas-gauche (15, 0)     - Joueur vert
        - Ruche 3 : coin bas-droite (15, 15)    - Joueur jaune
    
    Note:
        Chaque ruche contient : type, id, nectar initial, liste d'abeilles vide
    """
    ruche0 = {
        "type": "ruche",
        "id": "ruche0",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    ruche1 = {
        "type": "ruche",
        "id": "ruche1",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    ruche2 = {
        "type": "ruche",
        "id": "ruche2",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    ruche3 = {
        "type": "ruche",
        "id": "ruche3",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    #placer les ruches
    plateau[0][0].append(ruche0)
    plateau[0][NCASES-1].append(ruche1)
    plateau[NCASES-1][0].append(ruche2)
    plateau[NCASES-1][NCASES-1].append(ruche3)
    
    ruches = [ruche0, ruche1, ruche2, ruche3]
    return ruches

def creer_fleurs(NFLEURS):
    """
    Crée NFLEURS fleurs non encore placées sur le plateau.
    
    Les fleurs créées n'ont pas encore de position ni de nectar.
    Elles seront ensuite placées symétriquement par placer_fleurs().
    
    Args:
        NFLEURS (int): Nombre de fleurs à créer (par défaut 4)
    
    Returns:
        list: Liste de dictionnaires représentant les fleurs
              Chaque fleur : {"type": "fleur", "id": "fleurX", 
                             "nectar": 0, "position": None}
    
    Note:
        Le nectar sera attribué aléatoirement lors du placement
    """
    fleurs = []
    for i in range(NFLEURS):
        fleurs.append({
            "type": "fleur",
            "id": f"fleur{i}",
            "nectar": 0,
            "position": None
        })
    return fleurs

def placer_fleurs(plateau, fleurs):
    """
    Place les fleurs symétriquement sur le plateau et leur attribue du nectar.
    
    Pour chaque fleur, tire une position aléatoire dans le quart supérieur-gauche
    du plateau (hors zone protégée 4x4), puis crée 3 copies symétriques.
    Cela garantit que chaque joueur a la même disposition de fleurs.
    
    Args:
        plateau (list): Plateau de jeu 16x16
        fleurs (list): Fleurs créées par creer_fleurs()
    
    Algorithme:
        1. Pour chaque fleur, tirer (x, y) aléatoire dans le quart supérieur-gauche
        2. Vérifier que (x, y) n'est pas dans la zone protégée (0-3, 0-3)
        3. Calculer les 3 positions symétriques
        4. Vérifier qu'aucune fleur n'occupe déjà ces 4 positions
        5. Attribuer un nectar aléatoire entre 1 et MAX_NECTAR (45)
        6. Placer les 4 fleurs symétriques sur le plateau
    
    Symétries:
        - Position originale : (x, y)
        - Symétrie verticale : (N-1-x, y)
        - Symétrie horizontale : (x, N-1-y)
        - Symétrie centrale : (N-1-x, N-1-y)
    """
    #Placement de la fleur
    N = len(plateau)
    zone_protegee = 4
    for fleur in fleurs: #Pour chaque fleur
        position_valide = False
        while position_valide == False:
            x = random.randint(0, N//2) #on divise N par 2 pour ne prendre en compte que 1/4 du terrain (symétrie)
            y = random.randint(0, N//2)
            if x < zone_protegee and y < zone_protegee: #si l'aléatoire est DANS la zone protegees (ce qu'on ne veut pas)
                continue #recommencer le while jusqu'à position valide 
            positions = [ #pour créer la symétrie
                (x, y), #haut gauche
                (N-1-x, y), #symétrie verticale
                (x, N-1-y), #horizontale
                (N-1-x, N-1-y) #centrale ("diagonale")
            ]
            #-Vérification si la poisiton n'est pas déjà occupé par une FLEUR-
            toutes_libres = True
            for px, py in positions: #symétrie 
                for element in plateau[px][py]:
                    if element.get("type") == "fleur": #si la case est déjà occupé par une fleur
                        toutes_libres = False
                        break
                if toutes_libres == False:
                    break
            if toutes_libres == False:
                continue
            else:
                position_valide = True
                nectar = random.randint(1,MAX_NECTAR)
                #mettre à jour la fleur(dict) de base 
                fleur["nectar"] = nectar
                fleur["position"] = (x,y)
                #Créer les 3 symétriques
                fleur2 = {"type": "fleur", "id": fleur["id"], "nectar": nectar, "position": (N-1-x, y)}
                fleur3 = {"type": "fleur", "id": fleur["id"], "nectar": nectar, "position": (x, N-1-y)}
                fleur4 = {"type": "fleur", "id": fleur["id"], "nectar": nectar, "position": (N-1-x, N-1-y)}
                #Placer les 4 fleurs
                plateau[x][y].append(fleur)
                plateau[N-1-x][y].append(fleur2)
                plateau[x][N-1-y].append(fleur3)
                plateau[N-1-x][N-1-y].append(fleur4)

def creer_abeille(type_abeille, position, camp):
    """
    Crée une nouvelle abeille avec tous ses attributs initiaux.
    
    Args:
        type_abeille (str): "ouvriere", "eclaireuse" ou "bourdon"
        position (tuple): Position (x, y) sur le plateau
        camp (str): ID de la ruche propriétaire ("ruche0", "ruche1", etc.)
    
    Returns:
        dict: Dictionnaire représentant l'abeille avec ses attributs :
              - type : "abeille"
              - role : type d'abeille (ouvriere/eclaireuse/bourdon)
              - camp : ruche propriétaire
              - position : (x, y)
              - direction : "droite" (par défaut)
              - nectar : 0 (l'abeille ne transporte rien au départ)
              - etat : "OK" (active) ou "KO" (assommée)
              - a_bouge : False (peut bouger ce tour)
              - tours_ko_restants : 0
    
    Caractéristiques par type:
        - Ouvrière : capacité 12 nectar, force 1, 4 directions
        - Éclaireuse : capacité 3 nectar, force 1, 8 directions (diagonales)
        - Bourdon : capacité 1 nectar, force 5, 4 directions
    """
    abeille = {
        "type": "abeille",
        "role": type_abeille,
        "camp": camp,
        "position": position,
        "direction": "droite",
        "nectar": 0,
        "etat": "OK",
        "a_bouge": False,
        "tours_ko_restants": 0

    }
    return abeille

def placer_abeille(plateau,abeille):
    """
    Place une abeille sur le plateau à sa position.
    
    Args:
        plateau (list): Plateau de jeu
        abeille (dict): Abeille créée par creer_abeille()
    
    Note:
        L'abeille est ajoutée à la liste des éléments de sa case
    """
    x, y = abeille["position"]
    plateau[x][y].append(abeille)

def case_libre_abeille(plateau, x,y):
    """
    Vérifie qu'aucune abeille n'occupe la case (x, y).
    
    Args:
        plateau (list): Plateau de jeu
        x (int): Ligne de la case (0-15)
        y (int): Colonne de la case (0-15)
    
    Returns:
        bool: True si la case est libre (pas d'abeille), False sinon
    
    Note:
        Les fleurs et ruches ne bloquent pas, seules les abeilles comptent
    """
    for element in plateau[x][y]: #parcours les éléments dans la case
        if type(element) == dict and element.get("type") == "abeille": #si case == abeille
            return False
    return True

def distance_valide(pos1, pos2, distance_max=1, diagonale_autorisee=True):
    """
    Vérifie si la distance entre deux positions est valide pour un déplacement.
    
    Args:
        pos1 (tuple): Position de départ (x1, y1)
        pos2 (tuple): Position d'arrivée (x2, y2)
        distance_max (int): Distance maximale autorisée (par défaut 1)
        diagonale_autorisee (bool): True pour 8 directions, False pour 4
    
    Returns:
        bool: True si le déplacement est autorisé, False sinon
    
    Calculs:
        - Si diagonale autorisée (éclaireuse) : distance de Chebyshev
          max(|x2-x1|, |y2-y1|) <= distance_max
        - Sinon (ouvrière/bourdon) : distance de Manhattan
          |x2-x1| + |y2-y1| <= distance_max
    
    Exemples:
        >>> distance_valide((5, 5), (5, 6), 1, False)  # 1 case à droite
        True
        >>> distance_valide((5, 5), (6, 6), 1, False)  # Diagonale interdite
        False
        >>> distance_valide((5, 5), (6, 6), 1, True)   # Diagonale OK
        True
    """
    x1, y1 = pos1 #position 1(x,y)
    x2, y2 = pos2 #position 2(x,y), si la différence est + de 1 c pas bon.
    
    if diagonale_autorisee:
        # Distance de Chebyshev (8 directions)
        return max(abs(x2 - x1), abs(y2 - y1)) <= distance_max #return True or False
    else:
        # Distance de Manhattan (4 directions)
        return abs(x2 - x1) + abs(y2 - y1) <= distance_max
    
def dans_zone_ruche(position, joueur):
    """
    Vérifie si une position est dans la zone protégée d'une ruche (4x4).
    
    Args:
        position (tuple): Position à vérifier (x, y)
        joueur (int): Numéro du joueur (0, 1, 2 ou 3)
    
    Returns:
        bool: True si la position est dans la zone de la ruche du joueur
    
    Zones protégées:
        - Joueur 0 : x < 4 et y < 4 (haut-gauche)
        - Joueur 1 : x < 4 et y >= 12 (haut-droite)
        - Joueur 2 : x >= 12 et y < 4 (bas-gauche)
        - Joueur 3 : x >= 12 et y >= 12 (bas-droite)
    """
    x, y = position
    if joueur == 0:
        return x < 4 and y < 4
    elif joueur == 1:
        return x < 4 and y >= 12
    elif joueur == 2:
        return x >= 12 and y < 4
    elif joueur == 3:
        return x >= 12 and y >= 12

def calculer_cases_disponibles(abeille, plateau):
    """
    Calcule toutes les cases où l'abeille peut se déplacer.
    
    Args:
        abeille (dict): Abeille dont on veut connaître les déplacements possibles
        plateau (list): Plateau de jeu
    
    Returns:
        list: Liste de tuples (x, y) représentant les cases accessibles
    
    Vérifications effectuées:
        1. La case est dans le plateau (0-15)
        2. La case ne contient pas d'abeille
        3. La case n'est pas dans une zone ennemie (4x4 des autres ruches)
    
    Note:
        Les éclaireuses ont 8 directions (avec diagonales),
        les ouvrières et bourdons ont 4 directions (sans diagonales)
    """
    x_actuel, y_actuel = abeille["position"]
    cases_disponibles = []
    
    # Directions possibles
    if abeille["role"] == "eclaireuse":
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    else:
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    joueur_id = int(abeille["camp"][-1]) # ex: "ruche0" -> 0
    
    for dx, dy in directions:
        x_new = x_actuel + dx
        y_new = y_actuel + dy
        
        # 1. Vérifier limites plateau
        if 0 <= x_new < NCASES and 0 <= y_new < NCASES:
            
            # 2. Vérifier case libre 
            if not case_libre_abeille(plateau, x_new, y_new):
                continue
            
            # 3. Vérifier zones ennemies 
            zone_ennemie = False
            for i in range(4):
                if i != joueur_id:
                    if dans_zone_ruche((x_new, y_new), i):
                        zone_ennemie = True
                        break
            
            if not zone_ennemie:
                cases_disponibles.append((x_new, y_new))
    
    return cases_disponibles

# PHASE DE PONTE 

def tenter_ponte(plateau, ruche, type_abeille, position):
    """
    Tente de pondre une abeille dans la ruche.
    
    Vérifie que la ruche a assez de nectar (COUT_PONTE = 5) et que
    la case de la ruche est libre avant de créer l'abeille.
    
    Args:
        plateau (list): Plateau de jeu
        ruche (dict): Ruche qui veut pondre
        type_abeille (str): "ouvriere", "eclaireuse" ou "bourdon"
        position (tuple): Position de ponte (normalement la ruche)
    
    Returns:
        tuple: (abeille, None) si succès, (None, message_erreur) sinon
    
    Coût:
        Retire COUT_PONTE (5) points de nectar de la ruche
    
    Erreurs possibles:
        - "Pas assez de nectar ! (X/5)" si nectar < COUT_PONTE
        - "Case occupée !" si une abeille est déjà sur la case
    """
    #Vérifier si on a assez de nectar
    if ruche["nectar"] < COUT_PONTE:
        return None, f"Pas assez de nectar ! ({ruche["nectar"]}/{COUT_PONTE})"
    x,y = position
    #vérifier si la case est libre
    if case_libre_abeille(plateau, x,y) == False:
        return None, "Case occupée !"
    #sinon, créer l'abeille et la placer
    ruche["nectar"] -= COUT_PONTE
    abeille = creer_abeille(type_abeille, position, ruche["id"])
    ruche["abeilles"].append(abeille)
    placer_abeille(plateau, abeille)
    
    return abeille, None

def tenter_deplacement(plateau, abeille, nouvelle_position, ruches):
    """
    Tente de déplacer une abeille vers une nouvelle position.
    
    Vérifie la distance, que la case est libre et qu'on ne va pas
    en zone ennemie. Si l'abeille arrive dans sa zone de ruche,
    elle dépose automatiquement son nectar.
    
    Args:
        plateau (list): Plateau de jeu
        abeille (dict): Abeille à déplacer
        nouvelle_position (tuple): Position de destination (x, y)
        ruches (list): Liste des 4 ruches (pour déposer le nectar)
    
    Returns:
        tuple: (True, None) si succès, (False, message_erreur) sinon
    
    Vérifications:
        1. Distance valide (1 case max, diagonale selon le type)
        2. Case libre (pas d'abeille)
        3. Pas en zone ennemie (zone 4x4 des autres ruches)
    
    Effets:
        - Retire l'abeille de son ancienne case
        - Place l'abeille sur la nouvelle case
        - Marque a_bouge = True
        - Dépose le nectar si arrivée dans sa zone de ruche
    
    Erreurs possibles:
        - "Oula tu vas où là ? C'est trop loin !"
        - "Mhh.. y'a déjà quelqu'un sur la case"
        - "T'es un espion ? On est chez l'ennemi !"
    """
    x_old, y_old = abeille["position"]
    x_new, y_new = nouvelle_position

    # L'éclaireuse peut aller en diagonale, les autres non
    diagonale_ok = (abeille["role"] == "eclaireuse")

    # Vérifier distance
    if not distance_valide((x_old, y_old), (x_new, y_new), distance_max=1, diagonale_autorisee=diagonale_ok):
        return False, "Oula tu vas où là ? C'est trop loin !"

    # Vérifier case libre
    if not case_libre_abeille(plateau, x_new, y_new):
        return False, "Mhh.. y'a déjà quelqu'un sur la case"

    # Vérifier zones ennemies et dépôt nectar dans sa ruche
    joueur = int(abeille["camp"][-1])
    for i in range(4):
        if i != joueur and dans_zone_ruche(nouvelle_position, i):
            return False, "T'es un espion ? On est chez l'ennemie !"

    # Déplacer l'abeille
    plateau[x_old][y_old].remove(abeille)
    abeille["position"] = (x_new, y_new)
    abeille["a_bouge"] = True
    plateau[x_new][y_new].append(abeille)
    if dans_zone_ruche(nouvelle_position, joueur):
        deposer_nectar(abeille, ruches[joueur])

    return True, None



#====== BUTINAGE ======
def fleurs_accessibles(plateau, x,y):
    """
    Retourne toutes les fleurs accessibles depuis une position.
    
    Une fleur est accessible si elle est dans les 8 cases adjacentes
    (diagonales comprises) de la position (x, y).
    
    Args:
        plateau (list): Plateau de jeu
        x (int): Ligne de la position
        y (int): Colonne de la position
    
    Returns:
        list: Liste des fleurs accessibles (dictionnaires)
    
    Note:
        Même les fleurs vides (nectar = 0) sont retournées
    """
    fleurs = [] #va contenir TOUS les fleurs accessibles
    for dx in [-1, 0, 1]: #axe verticale
        for dy in [-1, 0, 1]: #axe horizontale, 8 DIRECTIONS 
            nx, ny = x + dx, y + dy #on ajoute x et y pour avoir les positions réelles de la case
            if 0 <= nx < NCASES and 0 <= ny < NCASES: #limiter les sorties de plateau
                for element in plateau[nx][ny]: #si il y a une fleur
                    if element["type"] == "fleur":
                        fleurs.append(element)
    return fleurs

def gain_nectar(fleur):
    """
    Calcule combien de nectar une abeille peut prendre sur une fleur.
    
    Le gain dépend de la quantité restante sur la fleur :
    - Fleur pleine (>= 2/3 de MAX_NECTAR) : 3 points
    - Fleur moyenne (> 1/3 et < 2/3) : 2 points  
    - Fleur presque vide (<= 1/3) : 1 point
    
    Args:
        fleur (dict): Fleur à butiner
    
    Returns:
        int: Nombre de points de nectar récoltés (1, 2 ou 3)
    
    Seuils (avec MAX_NECTAR = 45):
        - >= 30 nectar : gain de 3
        - 16-29 nectar : gain de 2
        - 1-15 nectar : gain de 1
    """
    if fleur["nectar"] >= (2*MAX_NECTAR) / 3: #si la fleur a plus de 2/3 de max_nectar
        return 3
    elif fleur["nectar"] > MAX_NECTAR / 3: #si la fleur a plus de 1/3 de max_nectar
        return 2
    return 1 #si la fleur a moins de 1/3 de max_nectar

def butiner(abeille, fleur):
    """
    Fait butiner une abeille sur une fleur.
    
    L'abeille prend du nectar selon gain_nectar(), mais ne peut pas
    dépasser sa capacité maximale. Le surplus est perdu (vandalisme).
    
    Args:
        abeille (dict): Abeille qui butine
        fleur (dict): Fleur à butiner
    
    Returns:
        int: Quantité de nectar effectivement prise par l'abeille
    
    Exemple:
        Une ouvrière (capacité 12) avec déjà 11 nectar butine une
        grosse fleur (gain de 3) :
        - Elle prend 1 nectar (car 11 + 1 = 12 max)
        - Les 2 autres points sont perdus
        - La fleur perd quand même 3 points (vandalisme)
    
    Capacités max:
        - Bourdon : 1
        - Éclaireuse : 3
        - Ouvrière : 12
    """
    #Savoir la capacité max selon le rôle
    max_cap = CAPACITE_NECTAR[abeille["role"]] #un chiffre
    #Gain potentiel de la fleur
    gain = gain_nectar(fleur)
    #place restante dans l'abeille
    place_restante = max_cap - abeille["nectar"]
    #quantité réellement stockée
    pris = min(gain, place_restante) 
    #mise à jour
    abeille["nectar"] += pris
    fleur["nectar"] -= gain #VANDALISME
    if fleur["nectar"] < 0: #limiter le negatif
        fleur["nectar"] = 0 
    return pris #retourne ce qui a été ajouté à l'abeille pour l'afficher

def deposer_nectar(abeille, ruche):
    """
    Dépose le nectar d'une abeille dans sa ruche si elle y est.
    
    Si l'abeille est dans la zone 4x4 de sa ruche, tout son nectar
    est transféré dans le stock de la ruche.
    
    Args:
        abeille (dict): Abeille qui veut déposer
        ruche (dict): Ruche de l'abeille
    
    Effet:
        - Ajoute abeille["nectar"] au stock de la ruche
        - Remet abeille["nectar"] à 0
    
    Note:
        Cette fonction est appelée automatiquement lors d'un déplacement
        dans la zone de ruche et à la fin de la phase de butinage
    """
    x,y = abeille["position"]
    joueur = int(ruche["id"][-1]) #prend le dernier caractère du dictionnaire ruche{i}
    if dans_zone_ruche((x,y), joueur) == True:
        ruche["nectar"] += abeille["nectar"]
        abeille["nectar"] = 0 

def tenter_butinage(plateau, abeille, ruche):
    """
    Tente de faire butiner une abeille.
    
    Vérifie que l'abeille n'a pas bougé ce tour et qu'une fleur
    est accessible avant de la faire butiner.
    
    Args:
        plateau (list): Plateau de jeu
        abeille (dict): Abeille qui veut butiner
        ruche (dict): Ruche de l'abeille (pour déposer le nectar)
    
    Returns:
        tuple: (True, nectar_pris) si succès, (False, message_erreur) sinon
    
    Vérifications:
        1. L'abeille n'a pas bougé (a_bouge = False)
        2. Au moins une fleur est accessible
    
    Effets:
        - Butine la première fleur accessible
        - Dépose le nectar si l'abeille est dans sa zone de ruche
        - Marque a_bouge = True
    
    Erreurs possibles:
        - "Cette abeille a bougé !"
        - "D'où voyez vous une fleur la ? Perso, j'en vois pas."
    """
    if abeille["a_bouge"] == True:
        return False, "Cette abeille a bougé !"
    x,y = abeille["position"]
    fleurs = fleurs_accessibles(plateau, x, y)

    if fleurs == []:
        return False, "D'où voyez vous une fleur la ? Perso, j'en vois pas."
    pris = butiner(abeille, fleurs[0])
    deposer_nectar(abeille, ruche)

    abeille["a_bouge"] = True
    
    return True, pris

#=== ESCARMOUCHE ===

def trouver_opposantes(plateau, abeille):
    """
    Trouve toutes les abeilles ennemies adjacentes à une abeille.
    
    Les opposantes sont les abeilles ennemies (camp différent) dans
    les 8 cases adjacentes (diagonales comprises) et en état OK.
    
    Args:
        plateau (list): Plateau de jeu
        abeille (dict): Abeille dont on cherche les opposantes
    
    Returns:
        list: Liste des abeilles ennemies adjacentes (max 8)
    
    Note:
        Les abeilles KO ne comptent pas comme opposantes
    """
    opposantes = [] #stock tous les ennemies
    x, y = abeille["position"]

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]: #les 8 directions
            if dx == 0 and dy == 0:#car c'est elle même 
                continue
            nx, ny = x + dx, y + dy #vrai position
            if 0 <= nx < NCASES and 0 <= ny < NCASES:#limiter sorti plateau
                for element in plateau[nx][ny]: #tous les élements de la cases
                    if (element["type"] == "abeille" and
                        element["camp"] != abeille["camp"] and
                        element["etat"] == "OK"): 
                        opposantes.append(element)
    return opposantes

def calculer_force_effective(abeille, opposantes):
    """
    Calcule la force effective d'une abeille en escarmouche.
    
    La force effective est la force de l'abeille divisée par le nombre
    d'opposantes, car elle divise son attaque entre toutes.
    
    Args:
        abeille (dict): Abeille en escarmouche
        opposantes (list): Liste des abeilles opposantes
    
    Returns:
        float: Force effective (FE = Force / nb_opposantes)
    
    Formule:
        FE = F / K  où F = force, K = nombre d'opposantes
    
    Exemples:
        - Bourdon (force 5) contre 2 ennemies : FE = 5/2 = 2.5
        - Ouvrière (force 1) contre 1 ennemie : FE = 1/1 = 1
        - Éclaireuse (force 1) sans ennemie : FE = 1 (force complète)
    """
    force = FORCE[abeille["role"]]
    nb_opposantes = len(opposantes)

    if nb_opposantes == 0: #pas d'ennemie
        return force #force complète
    return force/nb_opposantes #division pour calculer FE

def calculer_proba_esquive(abeille, opposantes, plateau):
    """
    Calcule la probabilité qu'une abeille esquive les attaques ennemies.
    
    La probabilité dépend de la force de l'abeille et de la somme
    des forces effectives de ses opposantes.
    
    Args:
        abeille (dict): Abeille qui tente d'esquiver
        opposantes (list): Liste des abeilles qui l'attaquent
        plateau (list): Plateau de jeu (pour calculer les FE ennemies)
    
    Returns:
        float: Probabilité d'esquive entre 0.0 et 1.0
    
    Formule:
        P(esquive) = F / (F + somme des FE ennemies)
        où F = force de l'abeille
    
    Exemple:
        Ouvrière (F=1) attaquée par un bourdon (FE=5/1=5) :
        P(esquive) = 1 / (1 + 5) = 1/6 ≈ 0.17 (17% de chances)
    
    Note:
        Si force totale = 0 (cas impossible), retourne 1.0 par sécurité
    """
    force = FORCE[abeille["role"]]
    #calcul la somme des FE des OPPOSANTES 
    somme_fe_ennemies = 0
    for opposante in opposantes:#Pour chaque opposante, trouver ses opposantes pour calculer sa FE
        opposantes_de_opposante = trouver_opposantes(plateau, opposante)
        fe = calculer_force_effective(opposante, opposantes_de_opposante)
        somme_fe_ennemies += fe
    #calcul de la probabilité d'esquive
    if force + somme_fe_ennemies == 0:
        return 1.0 # si y a zéro force des deux côtés, on dit que l’abeille esquive à 100%, éviter un crash
    
    return force / (force + somme_fe_ennemies)

def phase_escarmouche(plateau, ruche):
    """
    Gère la phase d'escarmouche pour toutes les abeilles d'une ruche.
    
    Pour chaque abeille de la ruche qui a des opposantes :
    1. Calcule sa probabilité d'esquive
    2. Tire un nombre aléatoire pour savoir si elle esquive
    3. Si échec : l'abeille perd son nectar et devient KO
    
    Args:
        plateau (list): Plateau de jeu
        ruche (dict): Ruche dont les abeilles sont en escarmouche
    
    Algorithme:
        1. Pour chaque abeille OK avec des opposantes :
           - Calculer sa probabilité d'esquive
           - Tirer aléatoirement (random entre 0 et 1)
           - Stocker le résultat (réussi/raté)
        
        2. Appliquer TOUS les résultats simultanément :
           - Les abeilles qui ont raté perdent leur nectar
           - Elles deviennent KO pour TIME_KO tours (5)
    
    Note:
        Les résultats sont appliqués simultanément pour éviter qu'une
        abeille KO dans la phase affecte les calculs des autres
    """
    resultats = [] #list des resultats de chaque abeille
    
    for abeille in ruche["abeilles"]:
        if abeille["etat"] != "OK": #si l'abeille est mort
            continue

        opposantes = trouver_opposantes(plateau, abeille) #stocker les ennemies

        if len(opposantes) == 0: #s'il n'y a pas d'ennemie
            continue #pas d'escarmouche

        #calcul proba d'esquive
        proba = calculer_proba_esquive(abeille, opposantes, plateau)
        #tirage
        tirage = random.random()#nombre entre 0 et 1
        esquive_reussie = tirage < proba #bool

        resultat = {
            "abeille": abeille,
            "esquive": esquive_reussie
        }
        resultats.append(resultat)
    
    #application des conséquences
    for resultat in resultats:
        abeille = resultat["abeille"]
        esquive_reussie = resultat["esquive"]
        if esquive_reussie == False: #esquive raté
            abeille["nectar"] = 0
            abeille["etat"] = "KO"
            abeille["tours_ko_restants"] = TIME_KO
#TOUR
def nouveau_tour(ruches):
    """
    Réinitialise toutes les abeilles pour un nouveau tour.
    
    Pour chaque abeille de chaque ruche :
    - Remet a_bouge à False (peut bouger à nouveau)
    - Décompte tours_ko_restants pour les abeilles KO
    - Réveille les abeilles dont le compteur KO atteint 0
    
    Args:
        ruches (list): Liste des 4 ruches du jeu
    
    Note:
        Appelé au début du tour du joueur 0 (quand tous ont joué)
    """
    for ruche in ruches:#chaque ruche
        for abeille in ruche["abeilles"]:#chaque abeille des ruches
            abeille["a_bouge"] = False #reset du a_bouge
            if abeille["etat"] == "KO":
                abeille["tours_ko_restants"] -= 1
                if abeille["tours_ko_restants"] <= 0:
                    abeille["etat"] = "OK"

def determiner_gagnant(ruches):
    """
    Retourne la ruche avec le plus de nectar.
    
    Args:
        ruches (list): Liste des 4 ruches
    
    Returns:
        dict: Ruche gagnante (celle avec le plus de nectar)
    
    Note:
        En cas d'égalité, c'est la première ruche trouvée qui gagne
    """
    gagnant = ruches[0] #on stock juste gagnant en tant que 1e ruche
    for ruche in ruches:
        if ruche["nectar"] > gagnant["nectar"]:
            gagnant = ruche #changement
    return gagnant

def fin_de_partie(plateau, ruches, tour, nectar_total_initial):
    """
    Vérifie si la partie est terminée selon les 3 conditions de victoire.
    
    Args:
        plateau (list): Plateau de jeu
        ruches (list): Liste des 4 ruches
        tour (int): Numéro du tour actuel
        nectar_total_initial (int): Nectar total au début de la partie
    
    Returns:
        tuple: (True, gagnant, raison) si fini, (False, None, None) sinon
    
    Conditions de fin (vérifiées dans cet ordre):
        1. "timeout" : tour >= TIME_OUT (300 tours)
        2. "blitzkrieg" : une ruche a > 50% du nectar initial
        3. "epuisement" : plus de nectar sur fleurs et abeilles
    
    Exemples:
        >>> fin_de_partie(plateau, ruches, 300, 180)
        (True, ruche_gagnante, "timeout")
        
        >>> ruches[0]["nectar"] = 95  # Plus de la moitié de 180
        >>> fin_de_partie(plateau, ruches, 50, 180)
        (True, ruches[0], "blitzkrieg")
    """
    # Condition 3 : Timeout
    if tour >= TIME_OUT:
        gagnant = determiner_gagnant(ruches)
        return True, gagnant, "timeout"
    
    # Condition 2 : Victoire blitzkrieg (plus de la moitié du nectar total)
    seuil_blitz = nectar_total_initial / 2
    for ruche in ruches:
        if ruche["nectar"] > seuil_blitz:
            return True, ruche, "blitzkrieg"
    
    # Condition 1 : Plus de nectar disponible
    nectar_restant = calculer_nectar_disponible(plateau, ruches)
    if nectar_restant == 0:
        gagnant = determiner_gagnant(ruches)
        return True, gagnant, "epuisement"
    
    return False, None, None

def calculer_nectar_disponible(plateau, ruches):
    """
    Calcule le nectar total encore en jeu (fleurs + abeilles).
    
    Le nectar dans les ruches NE COMPTE PAS (déjà récupéré).
    
    Args:
        plateau (list): Plateau de jeu
        ruches (list): Liste des 4 ruches
    
    Returns:
        int: Somme du nectar sur les fleurs et sur les abeilles
    
    Note:
        Utilisé pour vérifier la condition de fin "epuisement"
    """
    nectar_total = 0
    
    #nectar sur les fleurs
    for x in range(NCASES):
        for y in range(NCASES):
            for elem in plateau[x][y]:
                if isinstance(elem, dict) and elem.get("type") == "fleur":
                    nectar_total += elem["nectar"]
    
    #nectar sur les abeilles
    for ruche in ruches:
        for abeille in ruche["abeilles"]:
            nectar_total += abeille["nectar"]
    
    return nectar_total

def calculer_nectar_total_initial(plateau):
    """
    Calcule le nectar total au début de la partie (seulement les fleurs).
    
    Args:
        plateau (list): Plateau de jeu avec fleurs placées
    
    Returns:
        int: Somme du nectar de toutes les fleurs
    
    Note:
        À appeler juste après placer_fleurs() au début de la partie.
        Sert pour calculer la victoire "blitzkrieg" (> 50% du total)
    """
    nectar_total = 0
    for x in range(NCASES):
        for y in range(NCASES):
            for elem in plateau[x][y]:
                if isinstance(elem, dict) and elem.get("type") == "fleur":
                    nectar_total += elem["nectar"]
    return nectar_total

assert NCASES % 2 == 0, "NCASES doit être divisible par 2"
assert MAX_NECTAR % 3 == 0, "MAX_NECTAR doit être divisible par 3"
assert TIME_OUT % 4 == 0, "TIME_OUT doit être divisible par 4"
