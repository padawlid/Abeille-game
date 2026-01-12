#main.py GUI
"""
Interface graphique du jeu BZZZ.

Ce fichier gère tout l'affichage et les interactions :
- Chargement et affichage des images
- Dessin du plateau et des éléments
- Gestion des clics souris
- Animations et messages
- Menu de démarrage

La logique du jeu est dans model.py !
"""


from tkinter import *
from model import *
from ia import *

# =================================
# CONSTANTES GLOBALES
# =================================

COULEURS_RUCHES = {
    "ruche0": "bleu",
    "ruche1": "rouge", 
    "ruche2": "vert",
    "ruche3": "jaune"
}

TAILLE_SPRITE_ORIGINALE = 1024

POSITIONS_RUCHES = {
    0: (0, 0),
    1: (0, 15),
    2: (15, 0),
    3: (15, 15)
}


# =================================
# CHARGEMENT DES IMAGES
# =================================

def charger_image(chemin, taille_case):
    """
    Charge une image PNG et la redimensionne pour l'affichage.
    
    Utilise subsample() pour réduire l'image selon le ratio
    entre la taille originale (1024px) et la taille souhaitée.
    
    Args:
        chemin (str): Chemin du fichier image (ex: "image/fleur.png")
        taille_case (float): Taille d'une case en pixels (~43.75 pour 700/16)
    
    Returns:
        PhotoImage ou None: Image redimensionnée, ou None si fichier introuvable
    
    Exemple:
        >>> img = charger_image("image/fleur.png", 43.75)
        >>> # Image réduite d'un facteur 1024 / 43.75 ≈ 23
    
    Note:
        Les images PNG doivent faire 1024x1024 pixels à l'origine
    """
    try:
        ratio = TAILLE_SPRITE_ORIGINALE // int(taille_case)
        if ratio < 1:
            ratio = 1
        
        image = PhotoImage(file=chemin)
        image = image.subsample(ratio, ratio)
        
        return image
        
    except:
        print(f"Attention : {chemin} introuvable")
        return None


def charger_abeille(role, camp, direction, taille_case):
    """
    Charge l'image d'une abeille selon son type, sa ruche et sa direction.
    
    Args:
        role (str): "bourdon", "ouvriere" ou "eclaireuse"
        camp (str): "ruche0", "ruche1", "ruche2" ou "ruche3"
        direction (str): "droite" ou "gauche"
        taille_case (float): Taille d'une case en pixels
    
    Returns:
        PhotoImage ou None: Image de l'abeille redimensionnée
    
    Exemple de chemin:
        role="ouvriere", camp="ruche0", direction="droite"
        → "image/abeilles/ouvriere_bleu_droite.png"
    """
    couleur = COULEURS_RUCHES[camp]
    chemin = f"image/abeilles/{role}_{couleur}_{direction}.png"
    return charger_image(chemin, taille_case)


def charger_ruche(camp, taille_case):
    """
    Charge l'image d'une ruche selon sa couleur.
    
    Args:
        camp (str): "ruche0", "ruche1", "ruche2" ou "ruche3"
        taille_case (float): Taille d'une case en pixels
    
    Returns:
        PhotoImage ou None: Image de la ruche redimensionnée
    
    Couleurs:
        - ruche0 : bleu
        - ruche1 : rouge
        - ruche2 : vert
        - ruche3 : jaune
    """
    couleur = COULEURS_RUCHES[camp]
    chemin = f"image/ruches/ruche_{couleur}.png"
    return charger_image(chemin, taille_case)


def charger_toutes_images(taille_case):
    """
    Charge toutes les images nécessaires au jeu en une fois.
    
    Charge :
    - 4 images de ruches (une par couleur)
    - 1 image de fleur
    - 1 image de terrain (fond)
    - 24 images d'abeilles (3 types × 4 couleurs × 2 directions)
    
    Args:
        taille_case (float): Taille d'une case en pixels
    
    Returns:
        tuple: (images_ruches, image_fleur, images_abeilles, image_terre)
               où images_ruches et images_abeilles sont des dictionnaires
    
    Note:
        Affiche "Chargement des images..." puis "Images chargées !"
    """
    print("Chargement des images...")
    
    images_ruches = {}
    for ruche_id in COULEURS_RUCHES.keys():
        images_ruches[ruche_id] = charger_ruche(ruche_id, taille_case)
    
    image_fleur = charger_image("image/fleur.png", taille_case)
    image_terre = charger_image("image/terre_seamless.png", taille_case)
    
    images_abeilles = {}
    types_abeilles = ["bourdon", "ouvriere", "eclaireuse"]
    camps = ["ruche0", "ruche1", "ruche2", "ruche3"]
    directions = ["droite", "gauche"]
    
    for role in types_abeilles:
        for ruche_id in camps:
            for direction in directions:
                cle = f"{role}_{ruche_id}_{direction}"
                images_abeilles[cle] = charger_abeille(role, ruche_id, direction, taille_case)
    
    print("Images chargées !")
    
    return images_ruches, image_fleur, images_abeilles, image_terre


#=================================
# FONCTIONS DE DESSIN
#=================================

def dessiner_zones_protegees(canvas, taille_case, width, height):
    """
    Dessine les 4 zones protégées de 4x4 cases dans les coins.
    
    Ces zones sont colorées pour indiquer quelle ruche les possède.
    Les abeilles ennemies ne peuvent pas y entrer.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        taille_case (float): Taille d'une case en pixels
        width (int): Largeur totale du canvas en pixels
        height (int): Hauteur totale du canvas en pixels
    
    Couleurs des zones:
        - Haut-gauche (ruche 0) : bleu clair (#87CEEB)
        - Haut-droite (ruche 1) : rose/rouge (#FF5967)
        - Bas-gauche (ruche 2) : vert clair (#90EE90)
        - Bas-droite (ruche 3) : jaune (#FFFF99)
    """
    zone_size = 4 * taille_case
    
    canvas.create_rectangle(0, 0, zone_size, zone_size, fill="lightblue", outline="")
    canvas.create_rectangle(width - zone_size, 0, width, zone_size, fill="#FF5967", outline="")
    canvas.create_rectangle(0, height - zone_size, zone_size, height, fill="lightgreen", outline="")
    canvas.create_rectangle(width - zone_size, height - zone_size, width, height, fill="yellow", outline="")


def dessiner_quadrillage(canvas, width, height, taille_case):
    """
    Dessine les lignes noires du quadrillage 16x16.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        width (int): Largeur du canvas en pixels
        height (int): Hauteur du canvas en pixels
        taille_case (float): Taille d'une case en pixels
    
    Note:
        Dessine NCASES+1 lignes (17) car il faut une ligne de plus
        pour fermer le quadrillage (16 cases = 17 lignes)
    """
    for i in range(NCASES + 1):
        y = i * taille_case
        canvas.create_line(0, y, width, y, fill="#000000", width=2)
        x = i * taille_case
        canvas.create_line(x, 0, x, height, fill="#000000", width=2)


def dessiner_element(canvas, x, y, taille_case, image):
    """
    Dessine un élément (ruche/fleur/abeille) centré sur une case.
    
    Calcule le centre de la case (x, y) en pixels et y place l'image.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        x (int): Ligne de la case (0-15)
        y (int): Colonne de la case (0-15)
        taille_case (float): Taille d'une case en pixels
        image (PhotoImage): Image à dessiner
    
    Note:
        ATTENTION : en tkinter, les x et y sont inversés !
        centre_x = y * taille_case (colonne → horizontal)
        centre_y = x * taille_case (ligne → vertical)
    """
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x, centre_y, image=image)


def dessiner_fond_terrain(canvas, taille_case, image_terre):
    """
    Dessine le fond de terrain sur toutes les cases non protégées.
    
    Remplit le plateau avec une texture de terre, sauf dans les
    zones protégées 4x4 qui gardent leur couleur unie.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        taille_case (float): Taille d'une case en pixels
        image_terre (PhotoImage ou None): Texture de fond
    
    Note:
        Si image_terre est None, ne fait rien (pas de fond)
    """
    if image_terre is None:
        return
    
    for x in range(NCASES):
        for y in range(NCASES):
            # Vérifier si la case est dans une zone protégée
            dans_zone_protegee = False
            for i in range(4):
                if dans_zone_ruche((x, y), i):
                    dans_zone_protegee = True
                    break
            
            if not dans_zone_protegee:
                centre_x = y * taille_case + taille_case // 2
                centre_y = x * taille_case + taille_case // 2
                canvas.create_image(centre_x, centre_y, image=image_terre)


def dessiner_fond_abeille_ko(canvas, x, y, taille_case):
    """
    Dessine un fond rouge semi-transparent pour une abeille KO.
    
    Indique visuellement qu'une abeille est assommée sur cette case.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        x (int): Ligne de la case
        y (int): Colonne de la case
        taille_case (float): Taille d'une case en pixels
    
    Style:
        - Couleur : rouge (#FF4444)
        - Motif : points gris (stipple="gray50") pour transparence
    """

    x1 = y * taille_case
    y1 = x * taille_case
    x2 = x1 + taille_case
    y2 = y1 + taille_case
    
    canvas.create_rectangle(x1, y1, x2, y2, 
                          fill="#FF4444", stipple="gray50", 
                          outline="", width=0)


def dessiner_badge_nectar(canvas, x, y, taille_case, nectar):
    """
    Dessine un badge doré en haut à droite de la case avec le nectar.
    
    Affiche la quantité de nectar que l'abeille transporte sous
    forme d'un cercle doré avec un chiffre noir au centre.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        x (int): Ligne de la case de l'abeille
        y (int): Colonne de la case de l'abeille
        taille_case (float): Taille d'une case en pixels
        nectar (int): Quantité de nectar à afficher
    
    Style:
        - Cercle doré (#FFD700) avec bordure orange (#FF8C00)
        - Chiffre noir en gras, taille 10
        - Position : 8 pixels du bord haut-droite de la case
    """
    coin_x = (y + 1) * taille_case - 8
    coin_y = x * taille_case + 8
    
    canvas.create_oval(coin_x - 12, coin_y - 12, coin_x + 12, coin_y + 12,
                     fill="#FFD700", outline="#FF8C00", width=2)
    
    canvas.create_text(coin_x, coin_y, text=str(nectar),
                     font=("Arial", 10, "bold"), fill="#000000")


def dessiner_plateau(canvas, plateau, taille_case, images_ruches, image_fleur, images_abeilles, image_terre):
    """
    Parcourt tout le plateau et dessine chaque élément visible.
    
    Ordre de dessin (du fond vers le premier plan):
    1. Fond de terrain (sur cases non protégées)
    2. Fond rouge si abeille KO
    3. Ruches
    4. Fleurs
    5. Abeilles
    6. Badges de nectar (sur abeilles qui transportent)
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        plateau (list): Plateau de jeu 16x16
        taille_case (float): Taille d'une case en pixels
        images_ruches (dict): Dictionnaire des images de ruches
        image_fleur (PhotoImage): Image de fleur
        images_abeilles (dict): Dictionnaire des images d'abeilles
        image_terre (PhotoImage): Texture de fond
    
    Note:
        Parcourt les 256 cases (16×16) et tous leurs éléments
    """
    dessiner_fond_terrain(canvas, taille_case, image_terre)
    
    for x in range(NCASES):
        for y in range(NCASES):
            case = plateau[x][y]
            
            # Vérifier abeille KO
            abeille_ko = False
            for elem in case:
                if isinstance(elem, dict) and elem.get("type") == "abeille" and elem.get("etat") == "KO":
                    abeille_ko = True
                    break
            
            if abeille_ko:
                dessiner_fond_abeille_ko(canvas, x, y, taille_case)
            
            # Dessiner les éléments
            for element in case:
                if isinstance(element, dict):
                    if element["type"] == "ruche":
                        image = images_ruches.get(element["id"])
                        if image:
                            dessiner_element(canvas, x, y, taille_case, image)
                    
                    elif element["type"] == "fleur":
                        if image_fleur:
                            dessiner_element(canvas, x, y, taille_case, image_fleur)
                    
                    elif element["type"] == "abeille":
                        cle = f"{element['role']}_{element['camp']}_{element['direction']}"
                        image = images_abeilles.get(cle)
                        if image:
                            dessiner_element(canvas, x, y, taille_case, image)
                            
                            if element["nectar"] > 0:
                                dessiner_badge_nectar(canvas, x, y, taille_case, element["nectar"])


def dessiner_cases_disponibles(canvas, abeille, plateau, taille_case):
    """
    Dessine en vert les cases où l'abeille peut se déplacer.
    
    Aide visuelle pour le joueur pendant la phase de mouvement.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        abeille (dict): Abeille sélectionnée
        plateau (list): Plateau de jeu
        taille_case (float): Taille d'une case en pixels
    
    Style:
        - Couleur : vert foncé (#115511)
        - Motif : points gris (stipple="gray50") pour transparence
        - Bordure : vert (#115511), épaisseur 2
    """
    cases = calculer_cases_disponibles(abeille, plateau)
    
    for x_case, y_case in cases:
        x1 = y_case * taille_case
        y1 = x_case * taille_case
        x2 = x1 + taille_case
        y2 = y1 + taille_case
        
        canvas.create_rectangle(x1, y1, x2, y2, 
                              fill="#115511", stipple="gray50", 
                              outline="#115511", width=2)


def dessiner_selection_abeille(canvas, abeille, taille_case):
    """
    Dessine un cercle blanc autour de l'abeille sélectionnée.
    
    Indique visuellement quelle abeille est actuellement sélectionnée
    pour le déplacement.
    
    Args:
        canvas (Canvas): Canvas tkinter où dessiner
        abeille (dict): Abeille sélectionnée
        taille_case (float): Taille d'une case en pixels
    
    Style:
        - Cercle blanc (#FFFFFF)
        - Rayon : 25 pixels
        - Épaisseur : 4 pixels
    """

    x, y = abeille["position"]
    
    cx = y * taille_case + taille_case // 2
    cy = x * taille_case + taille_case // 2
    
    canvas.create_oval(cx - 25, cy - 25, cx + 25, cy + 25, 
                      outline="#FFFFFF", width=4)


# =================================
# GESTION DES MESSAGES ET LABELS
# =================================

def afficher_message(label_message, texte, couleur, fenetre):
    """
    Affiche un message temporaire pendant 2.5 secondes.
    
    Le message disparaît automatiquement après le délai.
    
    Args:
        label_message (Label): Label tkinter où afficher le message
        texte (str): Message à afficher
        couleur (str): Couleur du texte (ex: "#00FF00", "red")
        fenetre (Tk): Fenêtre principale (pour le timer)
    
    Exemples de messages:
        - "Ouvrière pondue !" en vert
        - "Pas assez de nectar !" en rouge
        - "Butiné ! +3" en vert
    """
    label_message.config(text=texte, fg=couleur)
    fenetre.after(2500, lambda: label_message.config(text=""))


def mettre_a_jour_label_tour(label_tour, tour_actuel):
    """
    Met à jour l'affichage du numéro de tour.
    
    Args:
        label_tour (Label): Label à mettre à jour
        tour_actuel (int): Numéro du tour en cours
    
    Format:
        "TOUR X / 300" (où 300 = TIME_OUT)
    """
    label_tour.config(text=f"TOUR {tour_actuel} / {TIME_OUT}")


def mettre_a_jour_label_phase(label_phase, phase, joueur_actuel, est_ia):
    """
    Met à jour l'affichage de la phase actuelle et du joueur.
    
    Change la couleur du label selon si c'est un humain ou une IA,
    et affiche la phase en cours (ponte/mouvement/butinage).
    
    Args:
        label_phase (Label): Label à mettre à jour
        phase (str): "ponte", "mouvement" ou "butinage"
        joueur_actuel (int): Numéro du joueur (0-3)
        est_ia (bool): True si le joueur est une IA
    
    Couleurs:
        - IA : orange (#FF8C00)
        - Joueur humain ponte : violet (#9B59B6)
        - Joueur humain mouvement : bleu (#3498DB)
        - Joueur humain butinage : vert (#27AE60)
    
    Format:
        "JOUEUR 1 - PHASE DE PONTE" ou "IA 2 - PHASE DE MOUVEMENT"
    """
    # Déterminer le préfixe
    joueur_num = joueur_actuel + 1

    if est_ia:
        prefix = "IA"
    else:
        prefix = "JOUEUR"
    
    # Déterminer la couleur et le nom selon la phase
    if phase == "ponte":
        if est_ia:
            couleur = "#FF8C00"
        else:
            couleur = "#9B59B6"
        nom_phase = "PONTE"

    elif phase == "mouvement":
        if est_ia:
            couleur = "#FF8C00"
        else:
            couleur = "#3498DB"
        nom_phase = "MOUVEMENT"

    elif phase == "butinage":
        if est_ia:
            couleur = "#FF8C00"
        else:
            couleur = "#27AE60"
        nom_phase = "BUTINAGE"

    label_phase.config(text=f"{prefix} {joueur_num} - PHASE DE {nom_phase}", 
                      bg=couleur, font=("Arial", 14, "bold"))


def mettre_a_jour_label_ruche(label, ruche, joueur_num, est_actif, est_joueur_actuel, est_ia):
    """
    Met à jour l'affichage des informations d'une ruche.
    
    Affiche le nectar, le nombre d'abeilles actives et KO.
    Met en évidence la ruche du joueur actuel.
    
    Args:
        label (Label): Label de la ruche à mettre à jour
        ruche (dict): Dictionnaire de la ruche
        joueur_num (int): Numéro du joueur (0-3)
        est_actif (bool): True si le joueur participe à la partie
        est_joueur_actuel (bool): True si c'est le tour de ce joueur
        est_ia (bool): True si c'est une IA
    
    Affichage:
        JOUEUR X / IA X
        
        Nectar: 25
        Abeilles actives: 8
        Abeilles KO: 2
        
        >>> A TON TOUR <<< (si joueur actuel)
    
    Style:
        - Joueur actuel : relief="sunken" (enfoncé)
        - Autres joueurs : relief="raised" (surélevé)
        - Joueurs inactifs : texte "JOUEUR INACTIF" en gris
    """
    if not est_actif:
        label.config(text="JOUEUR INACTIF", font=("Arial", 11, "bold"),
                   fg="#555555", relief="raised", borderwidth=3)
        return
    
    # Compter les abeilles actives
    nb_actives = 0
    for a in ruche["abeilles"]:
        if a["etat"] == "OK":
            nb_actives = nb_actives + 1
    
    # Compter les abeilles KO
    nb_ko = 0
    for a in ruche["abeilles"]:
        if a["etat"] == "KO":
            nb_ko = nb_ko + 1
    
    # Définir le prefix (IA ou JOUEUR)
    if est_ia:
        prefix = "IA"
    else:
        prefix = "JOUEUR"
    
    # Construire le texte selon si c'est le joueur actuel ou pas
    if est_joueur_actuel:
        texte = f"{prefix} {joueur_num + 1} \n\nNectar: {ruche['nectar']}\nAbeilles actives: {nb_actives}\nAbeilles KO: {nb_ko}\n\n>>> A TON TOUR <<<"
        label.config(text=texte, font=("Arial", 10, "bold"), relief="sunken", borderwidth=4)
    else:
        texte = f"{prefix} {joueur_num + 1}\n\nNectar: {ruche['nectar']}\nAbeilles actives: {nb_actives}\nAbeilles KO: {nb_ko}\n\n"
        label.config(text=texte, font=("Arial", 11, "bold"), relief="raised", borderwidth=3)


# =================================
# GESTION DES DÉPLACEMENTS AUTOMATIQUES
# =================================

def calculer_prochaine_case(abeille, destination, plateau):
    """
    Calcule la prochaine case pour se rapprocher d'une destination.
    
    Utilisé pour le système de prémove : l'abeille avance d'une case
    par tour vers sa destination programmée.
    
    Args:
        abeille (dict): Abeille qui se déplace
        destination (tuple): Position finale (x, y)
        plateau (list): Plateau de jeu
    
    Returns:
        tuple ou None: (x, y) de la prochaine case, ou None si impossible
    
    Algorithme:
        1. Calculer dx et dy (direction à prendre)
        2. Si éclaireuse : aller en diagonale si possible
        3. Sinon : avancer sur l'axe avec la plus grande distance
        4. Vérifier que la case est valide (libre, pas zone ennemie)
    
    Note:
        Retourne None si déjà arrivé, case bloquée ou zone ennemie
    """

    x_actuel, y_actuel = abeille["position"]
    x_dest, y_dest = destination
    
    if (x_actuel, y_actuel) == (x_dest, y_dest):
        return None
    
    # Calculer dx (direction horizontale)
    if x_dest == x_actuel:
        dx = 0
    elif x_dest > x_actuel:
        dx = 1
    else:
        dx = -1
    
    # Calculer dy (direction verticale)
    if y_dest == y_actuel:
        dy = 0
    elif y_dest > y_actuel:
        dy = 1
    else:
        dy = -1
    
    # Choisir la prochaine case selon le type d'abeille
    if abeille["role"] == "eclaireuse":
        prochaine = (x_actuel + dx, y_actuel + dy)
    else:
        dist_x = abs(x_dest - x_actuel)
        dist_y = abs(y_dest - y_actuel)
        
        if dist_x >= dist_y:
            prochaine = (x_actuel + dx, y_actuel)
        else:
            prochaine = (x_actuel, y_actuel + dy)
    
    x_new, y_new = prochaine
    
    if not (0 <= x_new < NCASES and 0 <= y_new < NCASES):
        return None
    
    if not case_libre_abeille(plateau, x_new, y_new):
        return None
    
    joueur = int(abeille["camp"][-1])
    for i in range(4):
        if i != joueur and dans_zone_ruche(prochaine, i):
            return None
    
    return prochaine


def executer_deplacements_automatiques(ruche, plateau, ruches):
    """
    Exécute un pas de déplacement pour toutes les abeilles programmées.
    
    Pour chaque abeille de la ruche qui a une destination programmée
    (attribut "destination_automatique"), tente de la déplacer d'une
    case vers sa destination.
    
    Args:
        ruche (dict): Ruche dont on déplace les abeilles
        plateau (list): Plateau de jeu
        ruches (list): Liste des 4 ruches
    
    Returns:
        bool: True si au moins une abeille a bougé, False sinon
    
    Note:
        Supprime "destination_automatique" de l'abeille quand elle arrive
    """
    abeilles_bougees = False
    
    for abeille in ruche["abeilles"]:
        if abeille["etat"] != "OK" or abeille["a_bouge"] or "destination_automatique" not in abeille:
            continue
        
        destination_finale = abeille["destination_automatique"]
        x_actuel, y_actuel = abeille["position"]
        
        prochaine_case = calculer_prochaine_case(abeille, destination_finale, plateau)
        
        if prochaine_case is None:
            continue
        
        x_new, y_new = prochaine_case
        
        if y_new > y_actuel:
            abeille["direction"] = "droite"
        elif y_new < y_actuel:
            abeille["direction"] = "gauche"
        
        succes, _ = tenter_deplacement(plateau, abeille, prochaine_case, ruches)
        
        if succes:
            abeilles_bougees = True
            if prochaine_case == destination_finale:
                del abeille["destination_automatique"]
    
    return abeilles_bougees


# =================================
# VERIFICATIONS AUTOMATIQUES
# =================================

def verifier_auto_skip_mouvement(ruche):
    """
    Vérifie si toutes les abeilles de la ruche ont bougé.
    
    Permet de passer automatiquement à la phase suivante si plus
    aucune abeille ne peut bouger.
    
    Args:
        ruche (dict): Ruche à vérifier
    
    Returns:
        bool: True si toutes les abeilles OK ont bougé, False sinon
    """
    for a in ruche["abeilles"]:
        if a["etat"] == "OK" and not a["a_bouge"]:
            return False
    return True


def verifier_auto_skip_butinage(ruche, plateau):
    """
    Vérifie si toutes les abeilles disponibles ont butiné.
    
    Permet de passer automatiquement à la phase suivante si plus
    aucune abeille ne peut butiner (pas de fleur accessible).
    
    Args:
        ruche (dict): Ruche à vérifier
        plateau (list): Plateau de jeu
    
    Returns:
        bool: True si toutes les abeilles OK ont butiné ou n'ont
              pas de fleur accessible, False sinon
    """
    for abeille in ruche["abeilles"]:
        if abeille["etat"] == "OK" and not abeille["a_bouge"]:
            x, y = abeille["position"]
            if fleurs_accessibles(plateau, x, y):
                return False
    return True


def verifier_peut_ponte(ruche):
    """
    Vérifie si la ruche a assez de nectar pour pondre.
    
    Args:
        ruche (dict): Ruche à vérifier
    
    Returns:
        bool: True si nectar >= COUT_PONTE (5), False sinon
    """
    return ruche["nectar"] >= COUT_PONTE


def verifier_a_abeille_active(ruche):
    """
    Vérifie si la ruche a au moins une abeille en état OK.
    
    Args:
        ruche (dict): Ruche à vérifier
    
    Returns:
        bool: True si au moins une abeille est active, False sinon
    
    Note:
        Utilisé pour sauter la phase de mouvement si plus d'abeilles
    """
    for abeille in ruche["abeilles"]:
        if abeille["etat"] == "OK":
            return True
    return False


# =================================
# GESTION DES CLICS
# =================================

def gerer_clic_selection_abeille(case, ruche, message_func, redessiner_func):
    """
    Gère la sélection d'une abeille en phase mouvement.
    
    Cherche dans la case cliquée une abeille du joueur qui peut bouger,
    et la sélectionne si trouvée.
    
    Args:
        case (list): Éléments présents sur la case cliquée
        ruche (dict): Ruche du joueur actuel
        message_func (function): Fonction pour afficher un message
        redessiner_func (function): Fonction pour redessiner (non utilisée ici)
    
    Returns:
        dict ou None: Abeille sélectionnée, ou None si aucune trouvée
    
    Conditions pour sélectionner une abeille:
        - Type = "abeille"
        - Camp = ruche du joueur
        - État = "OK" (pas KO)
        - a_bouge = False (n'a pas encore bougé)
    """
    for element in case:
        if (isinstance(element, dict) and 
            element.get("type") == "abeille" and
            element["camp"] == ruche["id"] and
            element["etat"] == "OK" and
            not element["a_bouge"]):
            
            message_func("Abeille sélectionnée ! Cliquez où aller !", "#00BFFF")
            return element
    
    return None


def gerer_clic_deplacement(abeille, x, y, plateau, ruches, message_func, redessiner_func):
    """
    Gère le déplacement d'une abeille vers une case cliquée.
    
    Si la case est adjacente : déplacement immédiat
    Si la case est lointaine : programmation d'un déplacement automatique
    
    Args:
        abeille (dict): Abeille sélectionnée à déplacer
        x (int): Ligne de la case de destination
        y (int): Colonne de la case de destination
        plateau (list): Plateau de jeu
        ruches (list): Liste des 4 ruches
        message_func (function): Fonction pour afficher un message
        redessiner_func (function): Fonction pour redessiner (non utilisée ici)
    
    Returns:
        bool: True si déplacement immédiat effectué (pour désélectionner),
              False si prémove programmé (garde la sélection)
    
    Fonctionnement:
        1. Met à jour la direction de l'abeille (droite/gauche)
        2. Vérifie si la case est adjacente (distance = 1)
        3. Si oui : déplacement immédiat
        4. Si non : ajoute "destination_automatique" à l'abeille
    """
    x_old, y_old = abeille["position"]
    
    if y > y_old:
        abeille["direction"] = "droite"
    elif y < y_old:
        abeille["direction"] = "gauche"
    
    diagonale_ok = (abeille["role"] == "eclaireuse")
    est_adjacent = distance_valide((x_old, y_old), (x, y), distance_max=1, diagonale_autorisee=diagonale_ok)
    
    if est_adjacent:
        succes, erreur = tenter_deplacement(plateau, abeille, (x, y), ruches)
        
        if not succes:
            message_func(erreur, "#FF4444")
            return False
        
        message_func("BZZZZZ, ON BOUGE !", "#00FF00")
        return True  
    
    else:
        abeille["destination_automatique"] = (x, y)
        message_func(f"Destination programmée vers ({x},{y})", "#FFD700")
        return False


def gerer_clic_butinage(case, ruche, plateau, message_func, redessiner_func):
    """
    Gère le clic pour faire butiner une abeille en phase butinage.
    
    Cherche une abeille du joueur sur la case cliquée qui peut butiner,
    et la fait butiner si possible.
    
    Args:
        case (list): Éléments présents sur la case cliquée
        ruche (dict): Ruche du joueur actuel
        plateau (list): Plateau de jeu
        message_func (function): Fonction pour afficher un message
        redessiner_func (function): Fonction pour redessiner le plateau
    
    Returns:
        bool: True si butinage effectué, False sinon
    
    Conditions pour butiner:
        - Abeille du joueur actuel
        - État OK
        - N'a pas bougé ce tour
        - Fleur accessible
    """
    for element in case:
        if (isinstance(element, dict) and
            element.get("type") == "abeille" and
            element["camp"] == ruche["id"] and
            element["etat"] == "OK" and
            not element["a_bouge"]):
            
            succes, resultat = tenter_butinage(plateau, element, ruche)
            
            if not succes:
                message_func(resultat, "#FF4444")
                return False
            
            message_func(f"Butiné ! +{resultat}", "#00FF00")
            redessiner_func()
            return True
    
    return False


# =================================
# FONCTION PRINCIPALE
# =================================

def afficher_plateau(plateau, ruches, tour_actuel, nectar_total_initial, config):
    """
    Crée et lance la fenêtre principale du jeu.
    
    C'est la fonction centrale qui initialise toute l'interface graphique
    et gère le déroulement de la partie.
    
    Args:
        plateau (list): Plateau de jeu 16x16
        ruches (list): Liste des 4 ruches
        tour_actuel (int): Numéro du tour de départ (toujours 1)
        nectar_total_initial (int): Nectar total au début (pour victoire)
        config (dict): Configuration {"nb_joueurs": int, "ia": [bool, bool, bool, bool]}
    
    Fonctionnement:
        1. Crée la fenêtre tkinter 1360x990 pixels
        2. Charge toutes les images
        3. Initialise les variables d'état (joueur, phase, abeille sélectionnée...)
        4. Crée les labels, canvas et boutons
        5. Définit toutes les fonctions locales (message, pondre, passer_phase...)
        6. Lance la boucle principale tkinter
    
    Variables d'état:
        - joueur_actuel : 0 à 3 (qui joue)
        - phase : "ponte", "mouvement" ou "butinage"
        - abeille_cliquee : None ou abeille sélectionnée
        - file_pontes : liste des pontes automatiques en attente
        - ias : [None ou IA_BZZZ] pour chaque joueur
    
    Fonctions imbriquées:
        - message() : affiche un message temporaire
        - redessiner() : redessine tout le plateau
        - afficher_boutons_ponte() : affiche/cache les boutons de ponte
        - pondre() : tente de pondre une abeille
        - passer_phase() : passe à la phase suivante
        - executer_escarmouche() : lance l'escarmouche et passe au joueur suivant
        - clic_plateau() : gère les clics sur le plateau
        - verifier_auto_skip() : vérifie si on peut auto-skip
        - jouer_ia_si_necessaire() : lance l'IA si c'est son tour
        - executer_tour_ia() : fait jouer l'IA pour la phase actuelle
    """
    
    # ========== CREATION DE LA FENÊTRE ==========
    
    fenetre = Tk()
    fenetre.title("BZZZ - Guerre des nahlas")
    fenetre.geometry("1360x990") # Fenêtre fixe 1360x990 pixels
    fenetre.resizable(False, False) # Empêche le redimensionnement
    fenetre.configure(bg="#2C2C2C")# Fond 
    # Calcul des dimensions du plateau
    width = 700 # Largeur du canvas en pixels
    height = width # Carré
    taille_case = width / NCASES

    # CHARGEMENT DES IMAGES
    images_ruches, image_fleur, images_abeilles, image_terre = charger_toutes_images(taille_case)
    
    # ========== VARIABLES D'ETAT ==========
    joueur_actuel = 0 # Joueur qui joue (0, 1, 2 ou 3)
    phase = "ponte" # Phase actuelle ("ponte", "mouvement", "butinage")
    abeille_cliquee = None # Abeille sélectionnée pour déplacement
    config_ia = config["ia"] # [bool, bool, bool, bool] : qui est IA
    nb_joueurs_actifs = config["nb_joueurs"] # Combien de joueurs (vrai humain) participent
    file_pontes = []  # File d'attente des pontes automatiques

    # Création des IAs (None si joueur humain)
    ias = []
    for i in range(4):
        if config_ia[i]:
            ias.append(creer_ia())
        else:
            ias.append(None)
    
    # ========== CREATION DE L'INTERFACE ==========
    
    label_tour = Label(fenetre, text="", font=("Arial", 18, "bold"),
                      bg="#1A1A1A", fg="#FFD700", pady=10)
    label_tour.grid(row=0, column=0, columnspan=3, sticky="ew")
    
    label_phase = Label(fenetre, text="", font=("Arial", 14, "bold"),
                       bg="#4A90E2", fg="white", pady=8)
    label_phase.grid(row=1, column=0, columnspan=3, sticky="ew")
    
    canvas = Canvas(fenetre, width=width-1, height=height-1, bg="green",
                   highlightthickness=2, highlightbackground="#000000")
    canvas.grid(row=2, column=1, padx=10, pady=10)
    
    frame_gauche = Frame(fenetre, width=270, bg="#2C2C2C")
    frame_gauche.grid(row=2, column=0, sticky="ns", padx=10)
    
    label_ruche0 = Label(frame_gauche, text="", bg="#87CEEB", font=("Arial", 11, "bold"),
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#000080", anchor="n", justify="left", padx=8, pady=8)
    label_ruche0.pack(pady=12, padx=5, fill="both", expand=True)
    
    label_ruche2 = Label(frame_gauche, text="", bg="#90EE90", font=("Arial", 11, "bold"),
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#006400", anchor="n", justify="left", padx=8, pady=8)
    label_ruche2.pack(pady=12, padx=5, fill="both", expand=True)
    
    frame_droite = Frame(fenetre, width=270, bg="#2C2C2C")
    frame_droite.grid(row=2, column=2, sticky="ns", padx=10)
    
    label_ruche1 = Label(frame_droite, text="", bg="#FFB6C1", font=("Arial", 11, "bold"),
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#8B0000", anchor="n", justify="left", padx=8, pady=8)
    label_ruche1.pack(pady=12, padx=5, fill="both", expand=True)
    
    label_ruche3 = Label(frame_droite, text="", bg="#FFFF99", font=("Arial", 11, "bold"),
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#8B6914", anchor="n", justify="left", padx=8, pady=8)
    label_ruche3.pack(pady=12, padx=5, fill="both", expand=True)
    
    labels_ruches = [label_ruche0, label_ruche1, label_ruche2, label_ruche3]
    
    frame_bas = Frame(fenetre, height=120, bg="#2C2C2C")
    frame_bas.grid(row=3, column=0, columnspan=3, pady=5, sticky="ew")
    frame_bas.grid_propagate(False)
    
    frame_boutons_ponte = Frame(frame_bas, bg="#2C2C2C", height=50)
    frame_boutons_ponte.pack(side=TOP, pady=(5, 0))
    
    btn_passer = Button(frame_bas, text="PASSER LA PHASE",
                       font=("Arial", 14, "bold"),
                       bg="#FF6B35", fg="white",
                       activebackground="#FF8C61", activeforeground="white",
                       width=30, height=2,
                       relief="raised", borderwidth=3,
                       cursor="hand2")
    btn_passer.pack(side=TOP, pady=(10, 5))
    
    label_message = Label(frame_bas, text="", font=("Arial", 11, "bold"),
                         bg="#2C2C2C", fg="#00FF00", height=1)
    label_message.pack(side=TOP, pady=(0, 5))
    
    # ========== FONCTIONS LOCALES ==========
    
    def message(texte, couleur="red"):
        """Affiche un message temporaire."""
        afficher_message(label_message, texte, couleur, fenetre)
    
    def redessiner():
        """Redessine tout le plateau et l'interface."""
        nonlocal joueur_actuel, phase, abeille_cliquee
        # Effacer le canvas
        canvas.delete("all")
        # Redessiner tout dans l'ordre
        dessiner_zones_protegees(canvas, taille_case, width, height)
        dessiner_plateau(canvas, plateau, taille_case, images_ruches, image_fleur, images_abeilles, image_terre)
        dessiner_quadrillage(canvas, width, height, taille_case)
        
        # Si une abeille est sélectionnée, montrer les cases disponibles
        if abeille_cliquee:
            if phase == "mouvement":
                dessiner_cases_disponibles(canvas, abeille_cliquee, plateau, taille_case)
            dessiner_selection_abeille(canvas, abeille_cliquee, taille_case)

        # Mettre à jour tous les labels
        mettre_a_jour_label_tour(label_tour, tour_actuel)
        
        est_ia = (ias[joueur_actuel] is not None)
        mettre_a_jour_label_phase(label_phase, phase, joueur_actuel, est_ia)
        
        for i in range(len(labels_ruches)):
            est_actif = (i < nb_joueurs_actifs)
            est_joueur_actuel = (i == joueur_actuel)
            est_ia_joueur = (ias[i] is not None)
            mettre_a_jour_label_ruche(labels_ruches[i], ruches[i], i, est_actif, est_joueur_actuel, est_ia_joueur)
        
        # Afficher/cacher les boutons de ponte
        afficher_boutons_ponte()
    
    def afficher_boutons_ponte():
        """Affiche les boutons de ponte si nécessaire."""
        widgets = frame_boutons_ponte.winfo_children()
        for widget in widgets:
            widget.destroy()
        
        # Si c'est une IA, ne rien afficher
        if ias[joueur_actuel] is not None:
            return
        
        # Afficher la file de ponte si elle existe
        if len(file_pontes) > 0:
            Label(frame_boutons_ponte,
                  text=f"File de ponte: {len(file_pontes)} en attente",
                  font=("Arial", 10, "bold"),
                  bg="#2C2C2C", fg="#FFD700").pack(side=TOP, pady=(0, 5))
        
        frame_btns = Frame(frame_boutons_ponte, bg="#2C2C2C")
        frame_btns.pack(side=TOP)
        
        # Bouton Ouvrière
        Button(frame_btns, text="OUVRIERE (5 nectars)", font=("Arial", 12, "bold"),
              bg="#8E44AD", fg="white", activebackground="#9B59B6",
              width=20, height=2, relief="raised", borderwidth=3,
              cursor="hand2", command=lambda: pondre("ouvriere")).pack(side=LEFT, padx=8)
        
        # Bouton Éclaireuse
        Button(frame_btns, text="ECLAIREUSE (5 nectars)", font=("Arial", 12, "bold"),
              bg="#3498DB", fg="white", activebackground="#5DADE2",
              width=20, height=2, relief="raised", borderwidth=3,
              cursor="hand2", command=lambda: pondre("eclaireuse")).pack(side=LEFT, padx=8)
        
        # Bouton Bourdon
        Button(frame_btns, text="BOURDON (5 nectars)", font=("Arial", 12, "bold"),
              bg="#E67E22", fg="white", activebackground="#F39C12",
              width=20, height=2, relief="raised", borderwidth=3,
              cursor="hand2", command=lambda: pondre("bourdon")).pack(side=LEFT, padx=8)

    def pondre(type_abeille):
        """Gère la ponte d'une abeille."""
        ruche = ruches[joueur_actuel]
        pos = POSITIONS_RUCHES[joueur_actuel]
        
        if phase == "ponte":
            abeille, erreur = tenter_ponte(plateau, ruche, type_abeille, pos)
            if erreur:
                message(erreur, "#FF4444")
            else:
                message(f"{type_abeille} pondu(e) !", "#00FF00")
                redessiner()
        else:
            file_pontes.append(type_abeille)
            message(f"{type_abeille} ajouté(e) à la file de ponte ({len(file_pontes)} en attente)", "#FFD700")
            redessiner()
    
    def passer_phase():
        """Passe à la phase suivante."""
        nonlocal joueur_actuel, phase, tour_actuel, abeille_cliquee
        
        abeille_cliquee = None # Désélectionner l'abeille
        ruche = ruches[joueur_actuel]
        
        if phase == "ponte":
            # 1. Gérer file de pontes automatiques
            if file_pontes:
                type_abeille = file_pontes[0]
                pos = POSITIONS_RUCHES[joueur_actuel]
                abeille, erreur = tenter_ponte(plateau, ruche, type_abeille, pos)
                
                if abeille:
                    file_pontes.pop(0)
                    message(f"{type_abeille} a rejoint la GUERRE automatiquement !", "#00FF00")
                    redessiner()
                    return
                else:
                    file_pontes.clear()
            
            # 2. Passage à la phase mouvement (TOUJOURS, même si pas assez de nectar)
            phase = "mouvement"
            
            if not verifier_a_abeille_active(ruche):
                passer_phase()
                return
        
        elif phase == "mouvement":
            abeilles_bougees = executer_deplacements_automatiques(ruche, plateau, ruches)
            
            if abeilles_bougees:
                redessiner()
                fenetre.update()
            
            phase = "butinage"
            
            peut_butiner = False
            for abeille in ruche["abeilles"]:
                if abeille["etat"] == "OK" and not abeille["a_bouge"]:
                    x, y = abeille["position"]
                    if fleurs_accessibles(plateau, x, y):
                        peut_butiner = True
                        break
            
            if not peut_butiner:
                passer_phase()
                return
        
        elif phase == "butinage":
            executer_escarmouche()
            return
        
        redessiner()
        jouer_ia_si_necessaire()
    
    def executer_escarmouche():
        """Exécute l'escarmouche et passe au joueur suivant."""
        nonlocal joueur_actuel, phase, tour_actuel
        
        phase_escarmouche(plateau, ruches[joueur_actuel])
        
        fini, gagnant, raison = fin_de_partie(plateau, ruches, tour_actuel, nectar_total_initial)
        if fini:
            label_gagnant = Label(fenetre, text="", font=("Arial", 20, "bold"),
                                bg="#FF6262", fg="#FFFFFF")
            label_gagnant.grid(row=0, column=0, columnspan=5, sticky="")
            
            messages_fin = {
                "timeout": f"{tour_actuel} tours terminés ! Joueur {int(gagnant['id'][-1])+1} gagne avec {gagnant['nectar']} nectar !",
                "blitzkrieg": f"VICTOIRE PAR DOMINATION ! Joueur {int(gagnant['id'][-1])+1} gagne avec {gagnant['nectar']} nectar !",
                "epuisement": f"RUPTURE DE STOCK ! Joueur {int(gagnant['id'][-1])+1} gagne avec {gagnant['nectar']} nectar !"
            }
            
            label_gagnant.config(text=messages_fin.get(raison, "FIN"))
            btn_passer.config(state="disabled")
            return
        
        joueur_actuel = (joueur_actuel + 1) % nb_joueurs_actifs
        
        if joueur_actuel == 0:
            tour_actuel += 1
            nouveau_tour(ruches)
        
        phase = "ponte"
        redessiner()
        jouer_ia_si_necessaire()
    
    def clic_plateau(event):
        """Gère les clics sur le plateau."""
        if ias[joueur_actuel] is not None:
            return
        
        nonlocal abeille_cliquee
        
        x = int(event.y / taille_case)
        y = int(event.x / taille_case)
        
        if not (0 <= x < NCASES and 0 <= y < NCASES):
            return
        
        ruche = ruches[joueur_actuel]
        case = plateau[x][y]
        
        if phase == "mouvement":
            if abeille_cliquee is None:
                abeille_cliquee = gerer_clic_selection_abeille(case, ruche, message, redessiner)
                if abeille_cliquee:
                    redessiner()
            else:
                succes = gerer_clic_deplacement(abeille_cliquee, x, y, plateau, ruches, message, redessiner)
                if succes: # Si succes == False (déplacement auto ou échec), on garde abeille_cliquee sélectionnée
                    abeille_cliquee = None
                    redessiner()
                    verifier_auto_skip()
        
        elif phase == "butinage":
            if gerer_clic_butinage(case, ruche, plateau, message, redessiner):
                verifier_auto_skip()
    
    def verifier_auto_skip():
        """Vérifie si on doit automatiquement passer à la phase suivante."""
        ruche = ruches[joueur_actuel]
        
        if phase == "mouvement" and verifier_auto_skip_mouvement(ruche):
            fenetre.after(20, passer_phase)
        
        elif phase == "butinage" and verifier_auto_skip_butinage(ruche, plateau):
            fenetre.after(20, passer_phase)
    
    def jouer_ia_si_necessaire():
        """Vérifie si le joueur actuel est une IA et lance son tour."""
        if ias[joueur_actuel] is not None:
            fenetre.after(20, executer_tour_ia)
    
    def executer_tour_ia():
        """Fait jouer l'IA pour la phase actuelle."""
        nonlocal phase, abeille_cliquee
        
        ia = ias[joueur_actuel]
        ruche = ruches[joueur_actuel]
        
        if phase == "ponte":
            file_pontes.clear()
            type_abeille = ia.jouer_tour_ponte(plateau, ruche)
            if type_abeille:
                pos = POSITIONS_RUCHES[joueur_actuel]
                abeille, erreur = tenter_ponte(plateau, ruche, type_abeille, pos)
                if not erreur:
                    message(f"IA {joueur_actuel+1} a pondu un(e) {type_abeille} !", "#FFA500")
                    redessiner()
                    fenetre.after(20, jouer_ia_si_necessaire)
                    return
            fenetre.after(20, passer_phase)
        
        elif phase == "mouvement":
            for abeille in ruche["abeilles"]:
                if "destination_automatique" in abeille:
                    del abeille["destination_automatique"]
            
            mouvements = ia.jouer_tour_mouvement(plateau, ruche, ruches)
            for abeille, nouvelle_pos in mouvements:
                x_old, y_old = abeille["position"]
                x_new, y_new = nouvelle_pos
                
                if y_new > y_old:
                    abeille["direction"] = "droite"
                elif y_new < y_old:
                    abeille["direction"] = "gauche"
                
                succes, _ = tenter_deplacement(plateau, abeille, nouvelle_pos, ruches)
                if succes:
                    redessiner()
                    fenetre.update()
            
            fenetre.after(20, passer_phase)
        
        elif phase == "butinage":
            abeilles = ia.jouer_tour_butinage(plateau, ruche)
            for abeille in abeilles:
                succes, resultat = tenter_butinage(plateau, abeille, ruche)
                if succes:
                    message(f"IA {joueur_actuel+1} a butiné +{resultat} !", "#FFA500")
                    redessiner()
                    fenetre.update()
            
            fenetre.after(20, passer_phase)
    
    # ========== LANCEMENT ==========
    
    btn_passer.config(command=passer_phase)
    canvas.bind("<Button-1>", clic_plateau)
    redessiner()
    jouer_ia_si_necessaire()
    fenetre.mainloop()


# =================================
# MENU DE DÉMARRAGE
# =================================

def menu_demarrage():
    """
    Affiche le menu de démarrage et retourne la configuration choisie.
    
    Propose différents modes de jeu :
    - 1 à 4 joueurs en hot-seat
    - Modes avec IA (1-3 joueurs + IA, ou 4 IA)
    
    Returns:
        dict: Configuration choisie {"nb_joueurs": int, "ia": [bool, bool, bool, bool]}
    
    Exemple:
        >>> config = menu_demarrage()
        >>> # Utilisateur choisit "2 JOUEURS + 2 IA"
        >>> config
        {"nb_joueurs": 4, "ia": [False, False, True, True]}
    
    Note:
        La fenêtre se ferme automatiquement quand un mode est choisi
    """

    menu = Tk()
    menu.title("BZZZ - Menu Principal")
    menu.geometry("600x950")
    menu.resizable(False, False)
    menu.configure(bg="#2C2C2C")
    
    choix_mode = {"nb_joueurs": 4, "ia": [False, False, False, False]}
    
    Label(menu, text="BZZZ - GUERRE DES ABEILLES", 
          font=("Arial", 24, "bold"), 
          bg="#2C2C2C", fg="#FFD700", pady=20).pack()
    
    Label(menu, text="Choisissez votre mode de jeu", 
          font=("Arial", 14), 
          bg="#2C2C2C", fg="white", pady=10).pack()
    
    frame_boutons = Frame(menu, bg="#2C2C2C")
    frame_boutons.pack(pady=30)
    
    def lancer_mode(nb_joueurs, config_ia):
        choix_mode["nb_joueurs"] = nb_joueurs
        choix_mode["ia"] = config_ia
        menu.destroy()
    
    boutons = [
        ("4 JOUEURS\n(Mode Hot-Seat)", "#27AE60", "#2ECC71", 4, [False, False, False, False]),
        ("3 JOUEURS\n(Ruche 4 désactivée)", "#3498DB", "#5DADE2", 3, [False, False, False, False]),
        ("2 JOUEURS\n(Ruches 3 et 4 désactivées)", "#9B59B6", "#AF7AC5", 2, [False, False, False, False]),
        ("1 JOUEUR\n(Seule Ruche 1 active)", "#E74C3C", "#EC7063", 1, [False, False, False, False]),
    ]
    
    for text, bg, active_bg, nb_j, ia_config in boutons:
        Button(frame_boutons, text=text, font=("Arial", 14 if nb_j == 4 else 13, "bold"),
              bg=bg, fg="white", activebackground=active_bg,
              width=25, height=3, relief="raised", borderwidth=4,
              cursor="hand2", command=lambda n=nb_j, c=ia_config: lancer_mode(n, c)).pack(pady=8)
    
    Label(frame_boutons, text="─── MODES AVEC IA ───", 
          font=("Arial", 12, "bold"), bg="#2C2C2C", fg="#888888").pack(pady=10)
    
    boutons_ia = [
        ("3 JOUEURS + 1 IA", "#5DADE2", "#85C1E9", [False, False, False, True]),
        ("2 JOUEURS + 2 IA", "#AF7AC5", "#D7BDE2", [False, False, True, True]),
        ("1 JOUEUR + 3 IA", "#E67E22", "#F39C12", [False, True, True, True]),
        ("4 IA (MODE SPECTATEUR)", "#95A5A6", "#BDC3C7", [True, True, True, True]),
    ]
    
    for text, bg, active_bg, ia_config in boutons_ia:
        Button(frame_boutons, text=text, font=("Arial", 13, "bold"),
              bg=bg, fg="white", activebackground=active_bg,
              width=25, height=2, relief="raised", borderwidth=4,
              cursor="hand2", command=lambda c=ia_config: lancer_mode(4, c)).pack(pady=6)
    
    Label(menu, text="Choisissez votre configuration", 
          font=("Arial", 10, "italic"), 
          bg="#2C2C2C", fg="#888888", pady=20).pack(side=BOTTOM)
    
    menu.mainloop()
    
    return choix_mode


def lancer_partie():
    """
    Lance une partie complète de BZZZ.
    
    C'est le point d'entrée du programme. Cette fonction :
    1. Affiche le menu de démarrage
    2. Récupère la configuration choisie
    3. Crée le plateau, les ruches et les fleurs
    4. Calcule le nectar total initial
    5. Lance l'interface graphique
    
    Affiche des informations de démarrage dans la console.
    """
    config = menu_demarrage()
    
    print("="*50)
    print("Lancement du jeu...")
    print(f"Nombre de joueurs humains: {config['nb_joueurs']}")
    print(f"Configuration IA: {config['ia']}")
    print("="*50)
    
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs(NFLEURS)
    placer_fleurs(plateau, fleurs)

    nectar_total_initial = calculer_nectar_total_initial(plateau)

    afficher_plateau(plateau, ruches, 1, nectar_total_initial, config)


if __name__ == "__main__":
    lancer_partie()
