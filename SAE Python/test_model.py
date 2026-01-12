# test_model.py - Tests unitaires pour BZZZ
"""
Tests unitaires pour le modèle du jeu BZZZ.

Ce fichier contient des tests pour vérifier que les fonctions
critiques de model.py fonctionnent correctement.

Tests implémentés:
    - Création du plateau
    - Zones de ruches
    - Distances valides
    - Ponte d'abeilles
    - Déplacement d'abeilles
    - Force effective
    - Fin de partie

Pour lancer les tests:
    python test_model.py
"""
from model import *

print("="*60)
print("TESTS UNITAIRES - BZZZ")
print("="*60)

# ============================================================================
# TESTS DE BASE
# ============================================================================

def test_creer_plateau():
    """
    Teste la création du plateau de jeu.
    
    Vérifie que:
        - Le plateau a exactement NCASES lignes (16)
        - Chaque ligne a exactement NCASES colonnes (16)
        - Toutes les cases sont vides au départ
    
    Returns:
        bool: True si tous les tests passent, False sinon
    
    Affiche "OK" si succès, ou un message d'erreur sinon
    """
    print("\nTest: creer_plateau()")
    plateau = creer_plateau()

    if len(plateau) != NCASES:
        print(f"ERREUR: {len(plateau)} lignes au lieu de {NCASES}")
        return False

    if not all(len(ligne) == NCASES for ligne in plateau): #all() = tout est vrai
        print("ERREUR: Mauvais nombre de colonnes")
        return False

    if not all(len(plateau[x][y]) == 0 for x in range(NCASES) for y in range(NCASES)):
        print("ERREUR: Certaines cases ne sont pas vides")
        return False

    print("OK")
    return True


def test_dans_zone_ruche():
    """
    Teste la détection des zones de ruches.
    
    Vérifie que:
        - (0, 0) et (3, 3) sont dans la zone de la ruche 0
        - (0, 15) et (3, 12) sont dans la zone de la ruche 1
        - (15, 0) et (12, 3) sont dans la zone de la ruche 2
        - (15, 15) et (12, 12) sont dans la zone de la ruche 3
        - (8, 8) n'est dans aucune zone de ruche
    
    Returns:
        bool: True si tous les tests passent, False sinon
    
    Affiche "X/5" où X est le nombre de tests réussis
    """
    print("\nTest: dans_zone_ruche()")

    tests = [
        dans_zone_ruche((0, 0), 0) and dans_zone_ruche((3, 3), 0),
        dans_zone_ruche((0, 15), 1) and dans_zone_ruche((3, 12), 1),
        dans_zone_ruche((15, 0), 2) and dans_zone_ruche((12, 3), 2),
        dans_zone_ruche((15, 15), 3) and dans_zone_ruche((12, 12), 3),
        not dans_zone_ruche((8, 8), 0) and not dans_zone_ruche((8, 8), 1)
    ]

    ok = sum(tests)
    total = len(tests)

    print(f"{ok}/{total}")
    return ok == total


def test_distance_valide():
    """
    Teste le calcul des distances valides pour les déplacements.
    
    Vérifie que:
        - Distance de 1 en ligne/colonne est valide sans diagonale
        - Distance de 1 en diagonale est invalide sans diagonale
        - Distance de 1 en diagonale est valide avec diagonale
        - Distance de 2 est toujours invalide
    
    Returns:
        bool: True si tous les tests passent, False sinon
    
    Affiche "X/4" où X est le nombre de tests réussis
    """
    print("\nTest: distance_valide()")

    tests = [
        distance_valide((5, 5), (5, 6), 1, False) and distance_valide((5, 5), (6, 5), 1, False),
        not distance_valide((5, 5), (6, 6), 1, False),
        distance_valide((5, 5), (6, 6), 1, True),
        not distance_valide((5, 5), (7, 5), 1)
    ]

    ok = sum(tests)
    total = len(tests)

    print(f"{ok}/{total}")
    return ok == total


# ============================================================================
# TESTS CRITIQUES
# ============================================================================

def test_tenter_ponte():
    """
    Teste la ponte d'abeilles.
    
    Crée un plateau et une ruche, puis teste:
        - Ponte réussie : crée une abeille, coûte COUT_PONTE nectar
        - Ponte échouée : refuse si nectar insuffisant
    
    Returns:
        bool: True si les 2 tests passent, False sinon
    
    Affiche "X/2" où X est le nombre de tests réussis
    """
    print("\nTest: tenter_ponte()")

    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    ruche = ruches[0]

    nectar_avant = ruche["nectar"]
    abeille, erreur = tenter_ponte(plateau, ruche, "ouvriere", (0, 0))

    ok1 = (
        abeille is not None
        and erreur is None
        and ruche["nectar"] == nectar_avant - COUT_PONTE
        and abeille in ruche["abeilles"]
    )

    ruche["nectar"] = 0
    abeille2, erreur2 = tenter_ponte(plateau, ruche, "bourdon", (0, 1))
    ok2 = abeille2 is None and erreur2 is not None

    ok = ok1 + ok2
    print(f"{ok}/2")
    return ok == 2


def test_tenter_deplacement():
    """
    Teste le déplacement d'abeilles.
    
    Crée un plateau avec une abeille, puis teste:
        - Déplacement réussi : déplace l'abeille d'une case
        - Déplacement échoué : refuse un déplacement trop lointain
    
    Returns:
        bool: True si les 2 tests passent, False sinon
    
    Affiche "X/2" où X est le nombre de tests réussis
    """
    print("\nTest: tenter_deplacement()")

    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    abeille = creer_abeille("ouvriere", (5, 5), "ruche0")
    placer_abeille(plateau, abeille)

    succes1, err1 = tenter_deplacement(plateau, abeille, (5, 6), ruches)
    ok1 = succes1 and err1 is None and abeille["position"] == (5, 6)

    succes2, err2 = tenter_deplacement(plateau, abeille, (8, 8), ruches)
    ok2 = not succes2 and err2 is not None

    ok = ok1 + ok2
    print(f"{ok}/2")
    return ok == 2


def test_calculer_force_effective():
    """
    Teste la fonction calculer_force_effective().

    Vérifie :
    - La force effective d'un bourdon face à deux abeilles opposantes.
    - La force effective d'un bourdon sans abeilles opposantes.
    
    Returns:
        bool : True si tous les tests passent, False sinon.
    """
    print("\nTest: calculer_force_effective()")

    bourdon = creer_abeille("bourdon", (5, 5), "ruche0")
    opposantes = [
        creer_abeille("ouvriere", (5, 6), "ruche1"),
        creer_abeille("ouvriere", (6, 5), "ruche1")
    ]

    ok1 = calculer_force_effective(bourdon, opposantes) == 5 / 2
    ok2 = calculer_force_effective(bourdon, []) == 5

    ok = ok1 + ok2
    print(f"{ok}/2")
    return ok == 2


def test_fin_de_partie():
    """
    Teste la fonction fin_de_partie().

    Vérifie :
    - La fin de partie déclenchée par un timeout.
    - La fin de partie déclenchée par un blitzkrieg (nectar >= 60).
    
    Returns:
        bool : True si tous les tests passent, False sinon.
    """
    print("\nTest: fin_de_partie()")

    plateau = creer_plateau()
    ruches = creer_ruche(plateau)

    fini1, _, r1 = fin_de_partie(plateau, ruches, TIME_OUT, 100)
    ok1 = fini1 and r1 == "timeout"

    ruches[0]["nectar"] = 60
    fini2, _, r2 = fin_de_partie(plateau, ruches, 10, 100)
    ok2 = fini2 and r2 == "blitzkrieg"

    ok = ok1 + ok2
    print(f"{ok}/2")
    return ok == 2


# ============================================================================
# LANCEMENT
# ============================================================================

def lancer_tous_les_tests():
    """
    Lance tous les tests définis pour le jeu.

    Affiche pour chaque test :
    - Le nom du test
    - "OK" si le test passe, "FAIL" sinon
    - Résultat final sous forme "réussis / total"

    Returns:
        None
    """
    print("\n" + "="*60)
    print("LANCEMENT DES TESTS")
    print("="*60)

    tests = [
        ("creer_plateau", test_creer_plateau()),
        ("dans_zone_ruche", test_dans_zone_ruche()),
        ("distance_valide", test_distance_valide()),
        ("tenter_ponte", test_tenter_ponte()),
        ("tenter_deplacement", test_tenter_deplacement()),
        ("calculer_force_effective", test_calculer_force_effective()),
        ("fin_de_partie", test_fin_de_partie())
    ]

    reussis = 0
    total = len(tests)

    for nom, resultat in tests:
        if resultat:
            reussis += 1
            print("OK", nom)
        else:
            print("FAIL", nom)

    print()
    print("RESULTAT:", reussis, "/", total)


if __name__ == "__main__":
    lancer_tous_les_tests()
