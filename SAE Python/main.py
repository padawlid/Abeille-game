from tkinter import *
from model import *



def dessiner_zones_protegees(canvas, taille_case, width, height):
    zone_size = 4 * taille_case
    
    # Coin haut-gauche
    canvas.create_rectangle(0, 0, zone_size, zone_size, fill="lightblue", outline="")
    
    # Coin haut-droite
    canvas.create_rectangle(width - zone_size, 0, width, zone_size, fill="red", outline="")
    
    # Coin bas-gauche
    canvas.create_rectangle(0, height - zone_size, zone_size, height, fill="lightgreen", outline="")
    
    # Coin bas-droite
    canvas.create_rectangle(width - zone_size, height - zone_size, width, height, fill="white", outline="")



def dessiner_quadrillage(canvas, width, height, taille_case):
    """Dessiner le quadrillage"""
    for i in range(NCASES + 1): #+1 car on a besoin de (NCASES + 1) ligne pour NCASES de case

        canvas.create_line(0, i*taille_case, width, i*taille_case, fill="black")
        canvas.create_line(i*taille_case, 0, i*taille_case, height,fill="black")



def dessiner_ruche(canvas, x, y, taille_case, image):
    #Calculer le centre de la case (x, y)
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    
    #Placer l'image au centre
    canvas.create_image(centre_x, centre_y, image=image)



def dessiner_fleur(canvas, x, y, taille_case, image):
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x,centre_y, image=image)


def dessiner_abeille(canvas,x,y,taille_case,image):
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x,centre_y, image=image)




def dessiner_plateau(canvas, plateau, taille_case, image_ruche, image_fleur, image_abeille):
    """
    Parcourt le plateau et dessine chaque élément
    """
    
    for x in range(NCASES):
        for y in range(NCASES):
            case = plateau[x][y]  # Liste d'éléments
            
            # Parcourir tous les éléments de la case
            for element in case:
                if type(element) is dict: #Vérifier si c'est une liste ou un dict direct
                    if element["type"] == "ruche":
                        dessiner_ruche(canvas, x, y, taille_case, image_ruche)
                    elif element["type"] == "fleur":
                        dessiner_fleur(canvas, x, y, taille_case, image_fleur)
                    elif element["type"] == "abeille":
                        dessiner_abeille(canvas, x, y, taille_case, image_abeille)


                    
def lancer_partie():
    # Initialisation
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs(NFLEURS)
    placer_fleurs(plateau, fleurs)
    
    # Pondre abeilles
    for ruche in ruches:
        abeille = pondre(ruche, "ouvriere", (0, 0))
        if abeille:
            placer_abeille(plateau, abeille)
    
    # Lancer l'affichage avec animation
    afficher_plateau_anime(plateau, ruches, 0)  # tour initial = 0


def afficher_plateau_anime(plateau, ruches, tour_actuel):
    fenetre = Tk()
    fenetre.title("BZZZZ...")
    fenetre.geometry("1600x800")
    
    # Images
    image_ruche = PhotoImage(file="image/ruche.png").subsample(10, 10) #divise par 10
    image_fleur = PhotoImage(file="image/fleur.png").subsample(10, 10)
    image_abeille = PhotoImage(file="image/abeille.png").subsample(10, 10)
    
    width = 800
    height = width
    taille_case = width / NCASES
    
    # CRÉER LE CANVAS ICI
    canvas = Canvas(fenetre, width=width-2, height=height-2, bg="green")
    canvas.pack()
    
    # MAINTENANT définir mettre_a_jour()
    def mettre_a_jour():
        nonlocal tour_actuel
        
        if tour_actuel < TIME_OUT:
            # Effacer le canvas
            canvas.delete("all")

            dessiner_zones_protegees(canvas, taille_case, width, height)
            
            # Redessiner quadrillage
            for i in range(NCASES + 1):
                canvas.create_line(0, i*taille_case, width, i*taille_case, fill="black")
                canvas.create_line(i*taille_case, 0, i*taille_case, height, fill="black")
            
            # Jouer le tour
            tour_jeu(plateau, ruches, tour_actuel)
            
            # Redessiner le plateau
            dessiner_plateau(canvas, plateau, taille_case, image_ruche, image_fleur, image_abeille)
            
            tour_actuel += 1
            
            # Planifier le prochain tour dans 1000ms
            fenetre.after(1000, mettre_a_jour)
    
    # Lancer la première mise à jour
    mettre_a_jour()
    fenetre.mainloop()


lancer_partie()
