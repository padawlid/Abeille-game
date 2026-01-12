# ia.py - Intelligence artificielle pour BZZZ

import random
from model import *

class IA_BZZZ:
    """
    Classe représentant une IA pour jouer à BZZZ.
    
    Cette IA utilise un système de scoring pour prendre ses décisions :
    - Ponte : Crée un équilibre entre ouvrières, éclaireuses et bourdons
    - Mouvement : Priorité au retour à la ruche si nectar, sinon recherche de fleurs
    - Butinage : Butine avec toutes les abeilles qui le peuvent
    """
    
    def __init__(self):
        """
        Crée une nouvelle instance d'IA.
        
        L'IA n'a pas besoin de mémoire entre les tours, donc __init__ est vide.
        """
        pass
    
    def jouer_tour_ponte(self, plateau, ruche):
        """
        Décide si l'IA veut pondre et quel type d'abeille créer.
        
        Args:
            plateau (list): Le plateau de jeu (liste 2D de cases)
            ruche (dict): La ruche de l'IA avec ses informations (nectar, abeilles)
        
        Returns:
            str ou None: Type d'abeille à pondre ("ouvriere", "eclaireuse", "bourdon")
                         ou None si pas de ponte ce tour
        
        Stratégie:
            - Vérifie d'abord si assez de nectar (minimum 20 pour garder une marge)
            - Si aucune abeille active : ponte obligatoire (type aléatoire)
            - Rush ouvrières en début de partie (moins de 4 abeilles)
            - Maintient un ratio optimal : 50% ouvrières, 25% éclaireuses, reste bourdons
        """
        # Vérifier si on a assez de nectar pour pondre
        if ruche["nectar"] < COUT_PONTE:
            return None
        
        # Compter les abeilles actives
        nb_actives = 0
        for a in ruche["abeilles"]:
            if a["etat"] == "OK":
                nb_actives += 1
        
        # Si aucune abeille active, on DOIT pondre (situation critique)
        if nb_actives == 0:
            types = ["ouvriere", "eclaireuse", "bourdon"]
            return random.choice(types)
        
        # Garder une marge de sécurité (ne pas tout dépenser)
        if ruche["nectar"] < COUT_PONTE + 15:
            return None
        
        # Début de partie : rush ouvrières pour collecter du nectar rapidement
        if nb_actives < 4:
            return "ouvriere"
        
        # Compter les types d'abeilles actives
        nb_ouvrieres = 0
        nb_eclaireuses = 0
        nb_bourdons = 0
        
        for abeille in ruche["abeilles"]:
            if abeille["etat"] == "OK":
                if abeille["role"] == "ouvriere":
                    nb_ouvrieres += 1
                elif abeille["role"] == "eclaireuse":
                    nb_eclaireuses += 1
                elif abeille["role"] == "bourdon":
                    nb_bourdons += 1
        
        # Calculer le total pour les ratios
        total = nb_ouvrieres + nb_eclaireuses + nb_bourdons
        if total == 0:
            return "ouvriere"
        
        # Ratio optimal : 50% ouvrières, 25% éclaireuses, 25% bourdons
        ratio_ouvriere = nb_ouvrieres / total
        ratio_eclaireuse = nb_eclaireuses / total
        
        # Priorité aux ouvrières (collecte de nectar)
        if ratio_ouvriere < 0.5:
            return "ouvriere"
        
        # Ensuite éclaireuses (mobilité et exploration)
        if ratio_eclaireuse < 0.25:
            return "eclaireuse"
        
        # Quelques bourdons pour la défense (si assez de nectar)
        if ruche["nectar"] > 30 and nb_bourdons < 2:
            return "bourdon"
        
        # Par défaut, créer des ouvrières
        return "ouvriere"
    
    def jouer_tour_mouvement(self, plateau, ruche, ruches):
        """
        Décide comment déplacer les abeilles de l'IA.
        
        Args:
            plateau (list): Le plateau de jeu
            ruche (dict): La ruche de l'IA
            ruches (list): Liste de toutes les ruches du jeu
        
        Returns:
            list: Liste de tuples (abeille, nouvelle_position)
        
        Stratégie:
            - Ne bouge pas les abeilles déjà sur une fleur (si elles ont de la place)
            - Pour les autres, calcule le meilleur mouvement via système de scoring
        """
        mouvements = []
        
        for abeille in ruche["abeilles"]:
            # Vérifier si l'abeille peut bouger
            if abeille["etat"] == "OK" and abeille["a_bouge"] == False:
                x, y = abeille["position"]
                fleurs = fleurs_accessibles(plateau, x, y)
                
                # Capacité max de l'abeille
                max_cap = CAPACITE_NECTAR[abeille["role"]]
                
                # Si une fleur est accessible ET qu'on a de la place
                # → On reste là pour butiner au prochain tour
                if len(fleurs) > 0 and abeille["nectar"] < max_cap:
                    continue
                
                # Sinon, trouver le meilleur mouvement
                mouvement = self._trouver_meilleur_mouvement(plateau, abeille, ruche, ruches)
                if mouvement:
                    mouvements.append((abeille, mouvement))
        
        return mouvements
    
    def _trouver_meilleur_mouvement(self, plateau, abeille, ruche, ruches):
        """
        Trouve le meilleur mouvement pour une abeille selon un système de scoring.
        
        Args:
            plateau (list): Le plateau de jeu (liste 2D de cases)
            abeille (dict): L'abeille à déplacer
            ruche (dict): La ruche du joueur actuel
            ruches (list): Liste de toutes les ruches
        
        Returns:
            tuple ou None: (x, y) position du meilleur mouvement,
                           ou None si aucun mouvement possible
        
        Fonctionnement:
            1. Liste toutes les cases adjacentes accessibles
            2. Élimine les cases hors plateau, occupées ou en zone ennemie
            3. Calcule un score pour chaque case restante
            4. Retourne la case avec le meilleur score
        """
        x, y = abeille["position"]
        joueur = int(ruche["id"][-1])  # Extraire le numéro du joueur (0-3)
        
        # Directions possibles selon le type d'abeille
        if abeille["role"] == "eclaireuse":
            # Éclaireuse : 8 directions (peut aller en diagonale)
            directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        else:
            # Ouvrière et Bourdon : 4 directions (pas de diagonale)
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
        
        cases_valides = []
        
        # Pour chaque direction possible
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            
            # Vérifier si la case est dans le plateau
            if nx < 0 or nx >= NCASES or ny < 0 or ny >= NCASES:
                continue
            
            # Vérifier si la case est libre (pas d'abeille dessus)
            case_libre = True
            for elem in plateau[nx][ny]:
                if isinstance(elem, dict) and elem.get("type") == "abeille":
                    case_libre = False
                    break
            
            if case_libre == False:
                continue
            
            # Vérifier qu'on n'est pas dans une zone ennemie
            zone_ennemie = False
            for i in range(4):
                if i != joueur and dans_zone_ruche((nx, ny), i):
                    zone_ennemie = True
                    break
            
            if zone_ennemie == False:
                # Case valide ! Calculer son score
                score = self._evaluer_case(plateau, (nx, ny), abeille, ruche, joueur)
                cases_valides.append(((nx, ny), score))
        
        # Si aucune case valide, rester sur place
        if len(cases_valides) == 0:
            return None
        
        # Choisir la case avec le meilleur score
        meilleure_case = cases_valides[0]
        for case_info in cases_valides:
            if case_info[1] > meilleure_case[1]:
                meilleure_case = case_info
        
        return meilleure_case[0]
    
    def _evaluer_case(self, plateau, position, abeille, ruche, joueur):
        """
        Évalue l'intérêt d'une case pour le déplacement d'une abeille.
        
        Args:
            plateau (list): Le plateau de jeu
            position (tuple): Position (x, y) à évaluer
            abeille (dict): L'abeille qui se déplace
            ruche (dict): La ruche du joueur
            joueur (int): Numéro du joueur (0-3)
        
        Returns:
            int: Score de la case (plus élevé = mieux)
        
        Système de scoring:
            Si l'abeille a du nectar (doit rentrer) :
                - +1000 si dans la zone de ruche (priorité absolue)
                - +score proportionnel à la proximité de la ruche
            
            Si l'abeille n'a pas de nectar (doit chercher fleurs) :
                - +80 par fleur adjacente contenant du nectar
                - +score selon proximité au centre du plateau (plus de fleurs)
            
            Dans tous les cas :
                - -15 par ennemi adjacent (zones dangereuses)
        """
        x, y = position
        score = 0
        
        # CAS 1 : Abeille a du nectar → PRIORITÉ au retour à la ruche
        if abeille["nectar"] > 0:
            # Si on est dans la zone de ruche, c'est PARFAIT
            if dans_zone_ruche(position, joueur):
                return 1000  # Score très élevé
            
            # Sinon, se rapprocher de la ruche
            ruche_pos = self._get_position_ruche(joueur)
            distance_ruche = abs(x - ruche_pos[0]) + abs(y - ruche_pos[1])
            score = score + (32 - distance_ruche) * 3  # Plus on est proche, mieux c'est
        
        # CAS 2 : Abeille sans nectar → Chercher des fleurs
        else:
            # Vérifier s'il y a des fleurs dans les 8 cases adjacentes
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx = x + dx
                    ny = y + dy
                    
                    if 0 <= nx < NCASES and 0 <= ny < NCASES:
                        for elem in plateau[nx][ny]:
                            if isinstance(elem, dict) and elem.get("type") == "fleur":
                                if elem["nectar"] > 0:
                                    score = score + 80  # Fleur proche = très bien
            
            # Se rapprocher du centre du plateau (statistiquement plus de fleurs)
            distance_centre = abs(x - 8) + abs(y - 8)
            score = score + (16 - distance_centre) * 2
        
        # PÉNALITÉ : Éviter les zones dangereuses (ennemis proches)
        nb_ennemis = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = x + dx
                ny = y + dy
                
                if 0 <= nx < NCASES and 0 <= ny < NCASES:
                    for elem in plateau[nx][ny]:
                        if isinstance(elem, dict) and elem.get("type") == "abeille":
                            if elem["camp"] != abeille["camp"] and elem["etat"] == "OK":
                                nb_ennemis = nb_ennemis + 1
        
        # Pénalité selon le nombre d'ennemis adjacents
        if nb_ennemis > 0:
            score = score - (nb_ennemis * 15)
        
        return score
    
    def _get_position_ruche(self, joueur):
        """
        Retourne la position de la ruche d'un joueur.
        
        Args:
            joueur (int): Numéro du joueur (0, 1, 2 ou 3)
        
        Returns:
            tuple: Position (x, y) de la ruche
        """
        if joueur == 0:
            return (0, 0)      # Ruche 0 : coin haut-gauche
        elif joueur == 1:
            return (0, 15)     # Ruche 1 : coin haut-droite
        elif joueur == 2:
            return (15, 0)     # Ruche 2 : coin bas-gauche
        else:  # joueur == 3
            return (15, 15)    # Ruche 3 : coin bas-droite
    
    def jouer_tour_butinage(self, plateau, ruche):
        """
        Décide quelles abeilles doivent butiner.
        
        Args:
            plateau (list): Le plateau de jeu
            ruche (dict): La ruche de l'IA
        
        Returns:
            list: Liste des abeilles qui vont butiner
        
        Stratégie:
            - Butine avec toutes les abeilles qui ont :
                1. Une fleur accessible (dans les 8 cases adjacentes)
                2. De la place dans leur réserve de nectar
        """
        abeilles_a_butiner = []
        
        for abeille in ruche["abeilles"]:
            # Vérifier si l'abeille peut butiner
            if abeille["etat"] == "OK" and abeille["a_bouge"] == False:
                x, y = abeille["position"]
                fleurs = fleurs_accessibles(plateau, x, y)
                
                # Si des fleurs sont disponibles
                if len(fleurs) > 0:
                    # Vérifier si l'abeille a de la place dans sa réserve
                    max_cap = CAPACITE_NECTAR[abeille["role"]]
                    if abeille["nectar"] < max_cap:
                        abeilles_a_butiner.append(abeille)
        
        return abeilles_a_butiner


def creer_ia():
    """
    Crée une instance d'IA pour jouer à BZZZ.
    
    Returns:
        IA_BZZZ: Une nouvelle instance d'IA
    
    Exemple d'utilisation:
        ia = creer_ia()
        type_abeille = ia.jouer_tour_ponte(plateau, ruche)
    """
    return IA_BZZZ()