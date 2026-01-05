# Modèle du jeu
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
    Créer un plateau de dimension NCASES (ici 16x16) avec les listes vides
    exemple:
    [[[],[],[],...(0-15)],
    [...]
    *15 aussi
    ]
    """
    plateau = []
    for _ in range(NCASES):
        ligne = []
        for _ in range(NCASES):
            ligne.append([])
        plateau.append(ligne)

def creer_ruche(plateau):
    """
    Créer les ruches(dict) qu'on va ensuite mettre dans notre plateau
    Settings donné aux ruches : type, id, nb de nectar, nb d'abeille
    """
    ruche0 = {
        "type": "ruche",
        "id": "ruche0",
        "nectar": NECTAR_INITIAL,
        "abeille": []
    }
    ruche1 = {
        "type": "ruche",
        "id": "ruche1",
        "nectar": NECTAR_INITIAL,
        "abeille": []
    }
    ruche2 = {
        "type": "ruche",
        "id": "ruche2",
        "nectar": NECTAR_INITIAL,
        "abeille": []
    }
    ruche3 = {
        "type": "ruche",
        "id": "ruche3",
        "nectar": NECTAR_INITIAL,
        "abeille": []
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
    Créer des fleurs (dict) avec paramètres:
    type
    id
    nectar et position (nectar ici à 0 et position None pour l'instant on va le changer dans placer_fleurs())
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
    Suite à creer_fleurs, on veut maintenant :
    - Placer les fleurs symétriquement sur le plateau en respectant leur condition (unicité des fleurs + en dehors de zones protegées)
    - Nectar est attribué entre 1 et MAX_NECTAR 
    - "Mettre" sur le plateau
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
    Créer UNE seule abeille (dict) avec ses settings
    """
    abeille = {
        "type": "abeille",
        "role": type_abeille,
        "camp": camp,
        "position": position,
        "etat": "OK",
        "a_bouger": False,
        "tours_ko_restants": 0
    }
    return abeille

def placer_abeille(plateau,abeille):
    """
    Placer l'abeille crée sur le plateau
    """
    x, y = abeille["position"]
    plateau[x][y].append(abeille)

def case_libre_abeille(plateau, x,y):
    """  
    Vérifie uniquement qu'aucune abeille occupe la case
    retourne TRUE si c bon sinon FALSE
    """
    for element in plateau[x][y]: #parcours les éléments dans la case
        if type(element) == dict and element.get("type") == "abeille": #si case == abeille
            return False
    return True

def distance_valide(pos1, pos2, distance_max=1): #(à voir pour debug de l'éclaireuse qui bouge sur 8 directions) maybe un max(..) <= distmax
    """  
    Vérifie si la distance entre deux positions est valide
    """
    x1, y1 = pos1 #position 1(x,y)
    x2, y2 = pos2 #position 2(x,y), si la différence est + de 1 c pas bon.
    return abs(x2 - x1) + abs(y2 - y1) <= distance_max #return True or False et regarde si c'est bien 1 case de bouger

def dans_zone_ruche(position, joueur):
    """  
    Vérifie si la position est dans la ruche du joueur
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
    
def tenter_ponte(plateau, ruche, type_abeille, position):
    """ 
    Tente de pondre une abeille dans une ruche sur le plateau
    Renvoie (abeille, None) si succès, (None, message d'erreur) sinon
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
    ruche["abeille"].append(abeille)
    placer_abeille(plateau, abeille)
    
    return abeille, None

def tenter_deplacement(plateau, abeille, nouvelle_position):
    """  
    Tente de déplacer l'abeille
    Renvoie (True, None) si succès, (False, message d'erreur) sinon
    """
    x_old, y_old = abeille["position"]
    x_new, y_new = nouvelle_position
    if distance_valide((x_old, y_old), (x_new, y_new)) == False:
        return False, "Oula tu vas où là ? C'est trop loin !"
    if case_libre_abeille(plateau, x_new, y_new) == False:
        return False, "Mhh.. y'a déjà quelqu'un sur la case"
    plateau[x_old][y_old].remove(abeille)
    abeille["position"] = (x_new, y_new)
    abeille["a_bouge"] = True
    plateau[x_new][y_new].append(abeille)

    return True, None
#====== BUTINAGE ======
def fleurs_accessibles(plateau, x,y):
    """  
    Retourne les fleurs accessibles pour l'abeille
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
    Définir combien de nectar l'abeille prend si elle choisie de butiner
    Retourne 3,2 ou 1
    """
    if fleur["nectar"] >= (2*MAX_NECTAR) / 3: #si la fleur a plus de 2/3 de max_nectar
        return 3
    elif fleur["nectar"] > MAX_NECTAR / 3: #si la fleur a plus de 1/3 de max_nectar
        return 2
    return 1 #si la fleur a moins de 1/3 de max_nectar

def butiner(abeille, fleur):
    """  
    Permet à une abeille de récolter du nectar 
    Le surplus est perdu (vandalisme), mais la guerre des abeilles est ce qu'elle est.
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
    Dépose le nectar de l'abeille dans sa ruche si elle y est
    """
    if abeille["camp"] != ruche["id"]:
        return
    x,y = abeille["position"]
    joueur = int(ruche["id"][-1]) #prend le dernier caractère du dictionnaire ruche{i}
    if dans_zone_ruche((x,y), joueur) == True:
        ruche["nectar"] += abeille["nectar"]
        abeille["nectar"] = 0 

def tenter_butinage(plateau, abeille, ruche):
    """  
    Tente de faire un butinage
    Retourne (True, nectar_pris) si succès, (False, erreur) sinon
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
    Détermine s'il y a des ennemies dans son rayon (8 cases adjacentes)
    """
    opposantes = [] #stock tous les ennemies
    x, y = abeille["position"]

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]: #les 8 directions
            if dx == 0 and dy == 0:#car c'est elle même mdr
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
    Calcule la force effective: FE = F(force de l'abeille) / nombre_opposantes
    """
    force = FORCE[abeille["role"]]
    nb_opposantes = len(opposantes)

    if nb_opposantes == 0: #pas d'ennemie
        return force #force complète
    return force/nb_opposantes #division pour calculer FE

def calculer_proba_esquive(abeille, opposantes, plateau):
    """  
    Calcul la probabilité d'esquive d'une abeille
    proba = F / (F + somme des FE ennemies)
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
    Gère la phase d'escarmouche pour UNE ruche
    1. Calcule toutes les probas d'esquive
    2. Tire au hasard pour chaque abeille
    3. Applique les conséquences
    """
    resultats = [] #list des resultats de chaque abeille
    
    for abeille in ruche["abeille"]:
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
    Réinitialise les abeilles pour un nouveau tour
    """
    for ruche in ruches:#chaque ruche
        for abeille in ruche["abeille"]:#chaque abeille des ruches
            abeille["a_bouge"] = False #reset du a_bouge
            if abeille["etat"] == "KO":
                abeille["tours_ko_restants"] -= 1
                if abeille["tours_ko_restants"] <= 0:
                    abeille["etat"] = "OK"

def determiner_gagnant(ruches):
    """  
    Retourne la ruche avec le plus de nectar
    """
    gagnant = ruches[0] #on stock juste gagnant en tant que 1e ruche
    for ruche in ruches:
        if ruche["nectar"] > gagnant["nectar"]:
            gagnant = ruche #changement
    return gagnant

def fin_de_partie(ruches, tour):
    """
    Vérifie si la partie est terminée.
    Retourne (True, gagnant) si fini, (False, None) sinon
    """
    if tour >= TIME_OUT:
        gagnant = determiner_gagnant(ruches)
        return True, gagnant
    return False, None

# console si jamais vérifier

# def lancer_partie():
#     plateau = creer_plateau()
#     ruches = creer_ruche(plateau)
#     fleurs = creer_fleurs(NFLEURS)
#     placer_fleurs(plateau, fleurs)
    
#     # Plus de code de test ici !
    
#     # Jouer les tours
#     for tour in range(1, TIME_OUT + 1):
#         tour_jeu(plateau, ruches, tour)
        
#         if fin_de_partie(ruches, tour):
#             break
# if __name__ == "__main__":
#     lancer_partie()
