#main.py comporte tout ce qui concerne l'affichage
from tkinter import *
from model import *

def dessiner_zones_protegees(canvas, taille_case, width, height):
    """  
    Permet de dessiner les zones protégées sur le plateau avec leur couleur
    """
    zone_size = 4 * taille_case
    #zone haut gauche 
    canvas.create_rectangle(0,0, zone_size, zone_size, fill="lightblue", outline="")
    #zone haut droite
    canvas.create_rectangle(width - zone_size, 0, width, zone_size, fill="#FF5967", outline="")
    #zone bas gauche
    canvas.create_rectangle(0, height - zone_size, zone_size, height, fill="lightgreen", outline="")
    #zone bas droite
    canvas.create_rectangle(width - zone_size, height - zone_size, width, height, fill="yellow", outline="")

def dessiner_quadrillage(canvas, width, height, taille_case):
    """  
    Dessiner le quadrillage sur le plateau
    """
    for i in range(NCASES + 1): # +1 car il en faut +1 de "|" pour une case 
        canvas.create_line(0, i*taille_case, width, i*taille_case, fill="black")
        canvas.create_line(i*taille_case, 0, i*taille_case, height, fill="black")

def dessiner_ruche(canvas, x, y, taille_case, image):
    """  
    Permet de placer la ruche sur sa case bien centré
    """
    #CALCUL du centre pixel (tkinter)
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    #Placer l'image au centre
    canvas.create_image(centre_x, centre_y, image=image)

def dessiner_fleur(canvas, x, y, taille_case, image):
    """  
    Pareil que dessiner ruche mais pour les fleurs
    """
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x,centre_y, image=image)

def dessiner_abeille(canvas,x,y,taille_case,image):
    """  
    Pareil que dessiner fleur mais pour les abeilles
    """
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x,centre_y, image=image)

def dessiner_plateau(canvas, plateau, taille_case, image_ruche, image_fleur, image_abeille):
    """
    Parcourt le plateau et dessine chaque élément
    """
    
    for x in range(NCASES): #ligne
        for y in range(NCASES): #colonne
            case = plateau[x][y]  # Liste d'éléments
            
            # Parcourir tous les éléments dans LA CASE
            for element in case:
                if type(element) is dict: #Vérifier si c'est une liste ou un dict direct
                    if element["type"] == "ruche":
                        dessiner_ruche(canvas, x, y, taille_case, image_ruche)
                    elif element["type"] == "fleur":
                        dessiner_fleur(canvas, x, y, taille_case, image_fleur)
                    elif element["type"] == "abeille":
                        dessiner_abeille(canvas, x, y, taille_case, image_abeille)

def afficher_plateau(plateau, ruches, tour_actuel):
    """  
    Création de la fenêtre avec TOUT
    """
    fenetre = Tk() 
    fenetre.title("BZZZZZZzZzZ") #titre de la fenêtre
    fenetre.geometry("1270x890")   # taille initiale
    fenetre.resizable(False, False)  # désactive agrandissement horizontal et vertical
    #Chargement des images :
    image_ruche = PhotoImage(file="image/ruche.png").subsample(10,10)
    image_fleur = PhotoImage(file="image/fleur.png").subsample(10,10)
    image_abeille = PhotoImage(file="image/abeille.png").subsample(10,10)
    #Dimension
    width = 700
    height = width #carré
    taille_case = width / NCASES #nombre de pixel 
    #Variable
    joueur_actuel = 0 #savoir qui joue
    phase = "ponte" #savoir à quel phase nous sommes
    abeille_cliquee = None #savoir qui est selectionné
    POSITIONS_RUCHES = {0: (0,0), 
                        1: (0,15), 
                        2: (15,0), 
                        3: (15,15)}
    #Interface
    label_tour = Label(fenetre, text="", font=("Arial", 16))
    label_tour.grid(row=0, column=0, columnspan=3, sticky="ew")

    label_phase = Label(fenetre, text="", font=("Arial", 12, "bold"), bg="#FF54D0", fg="white", pady=5)
    label_phase.grid(row=1, column=0, columnspan=3, sticky="ew")
    
    #plateau centré
    canvas = Canvas(fenetre, width=width, height=height, bg="green")
    canvas.grid(row=2, column=1, padx=10, pady=10)
    
    #Info ruches gauches
    frame_gauche = Frame(fenetre, width=250)
    frame_gauche.grid(row=2, column=0, sticky="ns", padx=10)

    # Ruche 0 (haut-gauche) en haut
    label_ruche0 = Label(frame_gauche, text="", bg="lightblue", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche0.pack(pady=15, padx=5, fill="both", expand=True)

    # Ruche 2 (bas-gauche) en bas
    label_ruche2 = Label(frame_gauche, text="", bg="lightgreen", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche2.pack(pady=15, padx=5, fill="both", expand=True)

    # Infos ruches droite (ruches du côté droit du plateau)
    frame_droite = Frame(fenetre, width=250)
    frame_droite.grid(row=2, column=2, sticky="ns", padx=10)

    # Ruche 1 (haut-droite) en haut
    label_ruche1 = Label(frame_droite, text="", bg="#FF5967", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche1.pack(pady=15, padx=5, fill="both", expand=True)

    # Ruche 3 (bas-droite) en bas
    label_ruche3 = Label(frame_droite, text="", bg="yellow", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche3.pack(pady=15, padx=5, fill="both", expand=True)

    labels_ruches = [label_ruche0, label_ruche1, label_ruche2, label_ruche3]

    #Frame pour boutons et message
    frame_bas = Frame(fenetre)
    frame_bas.grid(row=3, column=0, columnspan=3, pady=10)
    label_message = Label(frame_bas, text="", font=("Arial", 10), fg="red")
    label_gagnant = Label(fenetre, text="", font=("Arial", 16), fg="green")
    label_gagnant.grid(row=4, column=0, columnspan=3)
    #== FONCTIONS LOCALES ==
    def message(texte, couleur="red"):
        """  
        On donne un texte et sa couleur et ça converti en texte 
        qu'on peut voir sur le jeu
        """
        label_message.config(text=texte, fg=couleur)
        fenetre.after(2000, lambda: label_message.config(text=""))

    def passer_phase():
        """  
        Permet de passer à la phase suivante
        """
        nonlocal joueur_actuel, phase, tour_actuel, abeille_cliquee
        abeille_cliquee = None
        if phase == "ponte":
            phase = "mouvement"
            #vérifier s'il existe au moins une abeille OK
            a_une_abeille = False
            for abeille in ruches[joueur_actuel]["abeilles"]:
                if abeille["etat"] == "OK":
                    a_une_abeille = True
                    break
            if a_une_abeille == False:
                passer_phase()
                return
        
        elif phase == "mouvement":
            phase = "butinage"
            #vérifier s'il existe une abeille OK qui n'a pas bougé
            a_une_abeille_dispo = False
            for abeille in ruches[joueur_actuel]["abeilles"]:
                if abeille["etat"] == "OK" and abeille["a_bouge"] == False:
                    a_une_abeille_dispo = True
                    break
            if a_une_abeille_dispo == False:
                passer_phase()
                return
            
        elif phase == "butinage":
            phase = "escarmouche"
            redessiner()
            executer_escarmouche()
            return
        redessiner()

    def executer_escarmouche():
        """  
        Cette fonction termine le tour d'un joueur, passe au suivant,
        gère le changement de tour, vérifie la victoire puis relance la phase de ponte
        """
        nonlocal joueur_actuel, phase, tour_actuel
        phase_escarmouche(plateau, ruches[joueur_actuel])
        joueur_actuel = (joueur_actuel + 1)%4 #modulo pour garder 0,1,2,3

        if joueur_actuel == 0: #nouveau tour (joueur 0)
            tour_actuel += 1
            nouveau_tour(ruches)
        phase = "ponte"
        if tour_actuel >= TIME_OUT:
            gagnant = determiner_gagnant(ruches)
            label_gagnant.config(text=f" GG {gagnant["id"]} ! Il possède {gagnant['nectar']} nectar !")
            return
        redessiner()
    def pondre(type_abeille):
        """  
        Utilise la fonction tenter_pondre pour l'appliquer au plateau
        """
        ruche = ruches[joueur_actuel]
        pos = POSITIONS_RUCHES[joueur_actuel]
        _, erreur = tenter_ponte(plateau, ruche, type_abeille, pos) #"_" est inutile, on veut savoir si ya erreur c tout 
        if erreur:
            message(erreur)
            return
        else:
            message(f"{type_abeille} viens de rejoindre cette guerre !", "green")
            redessiner()

    def clic_plateau(event): 
        """  
        Event = position de notre click
        Cette fonction permet de gérer tout ce qui parle de l'interaction "click"
        """
        nonlocal abeille_cliquee #on reprend ce qu'on a stocké DANS la fonction
        #plateau[ligne(event.y)][colonne(event.x)]
        x = int(event.y / taille_case) #colonne pas en float
        y = int(event.x / taille_case) #ligne pas en float (d'où le int())
        if x < 0 or x >= NCASES or y < 0 or y >= NCASES: #Si c'est en dehors du plateau
            return
        ruche = ruches[joueur_actuel]
        case = plateau[x][y]
        #Les phases peuvent être : ponte, mouvement ou butinage
        if phase == "mouvement":
            if abeille_cliquee == None: #Si on a pas encore sélectionner d'abeille à bouger
                for element in case: #on parle bien de la case que nous avons "cliqué"
                    if (isinstance(element,dict) and element.get("type") == "abeille" and #isinstance et .get pour sécurité crash
                        element["camp"] == ruche["id"] and element["etat"] == "OK" and 
                        element["a_bouge"] == False):
                        abeille_cliquee = element
                        message("Vous avez sélectionné cette abeille ! Cliquez où aller !", "blue")
                        redessiner()
                        return
            else:
                succes, erreur = tenter_deplacement(plateau, abeille_cliquee, (x,y))
                if erreur:
                    message(erreur)
                    return
                message("C'est bon il a bougé !", "green")
                abeille_cliquee = None #reset
                redessiner()
        elif phase == "butinage":
            for element in case:
                if (isinstance(element,dict) and element.get("type") == "abeille" and
                    element["camp"] == ruche["id"] and element["etat"] == "OK" and
                    element["a_bouge"] == False):
                    succes, resultat = tenter_butinage(plateau, element, ruche)
                    if succes == False:
                        message(resultat)
                        return
                    else:
                        message(f"Butinèx ! +{resultat}", "green")
                        redessiner()
                        return

    def redessiner():
        """  
        Permet de faire animé le plateau
        On supprime tout et on remet avec l'update :)
        """
        canvas.delete("all")
        dessiner_zones_protegees(canvas, taille_case, width, height)
        dessiner_quadrillage(canvas, width, height, taille_case)
        dessiner_plateau(canvas, plateau, taille_case, image_ruche, image_fleur, image_abeille)
        if abeille_cliquee:
            x, y = abeille_cliquee["position"]
            cx = y * taille_case + taille_case / 2
            cy = x * taille_case + taille_case / 2
            canvas.create_oval(cx-20, cy-20, cx+20, cy+20, outline="red", width=3)
        
        label_tour.config(text=f"Tour {tour_actuel}/{TIME_OUT}")
        
        ruche = ruches[joueur_actuel]
        if phase == "ponte":
            label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - PONTE : Pondre ou passer", font=("Arial", 15, "bold"))
            btn_ouvriere.pack(side=LEFT, padx=5)
            btn_eclaireuse.pack(side=LEFT, padx=5)
            btn_bourdon.pack(side=LEFT, padx=5)
        else:
            btn_ouvriere.pack_forget()
            btn_eclaireuse.pack_forget()
            btn_bourdon.pack_forget()
            
            if phase == "mouvement":
                label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - MOUVEMENT : Cliquez abeille puis case")
            elif phase == "butinage":
                label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - BUTINAGE : Cliquez abeille pour butiner")
            elif phase == "escarmouche":
                label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - ESCARMOUCHE...")
        
        btn_passer.pack(side=TOP, pady=10)
        label_message.pack(side=RIGHT)
        
        for i in range(len(labels_ruches)):
            label = labels_ruches[i]
            ruche = ruches[i]

            # Compter les abeilles actives et KO
            nb_actives = 0
            nb_ko = 0
            for abeille in ruche["abeilles"]:
                if abeille["etat"] == "OK":
                    nb_actives += 1
                elif abeille["etat"] == "KO":
                    nb_ko += 1

            # Mettre à jour le texte du label
            if i == joueur_actuel:
                label.config(text="Joueur {} (à ton tour)\n\nNectar: {}\nAbeilles actives: {}\nAbeilles KO: {}".format(
                        (int(ruche["id"][-1])+1), ruche["nectar"], nb_actives, nb_ko
                    ),
                    font=("Arial", 12, "bold"), fg='#9E0000')
            else:
                label.config(text="Joueur {}\n\nNectar: {}\nAbeilles actives: {}\nAbeilles KO: {}".format(
                        (int(ruche["id"][-1])+1), ruche["nectar"], nb_actives, nb_ko
                    ),
                    font=("Arial", 11, "bold"), fg='#000000')
    #Créer les boutons !
    btn_ouvriere = Button(frame_bas, text=" Pondre Ouvrière ! (5 nectars) ", font=("Arial", 10, "bold"),
                          bg="#3F00A5", fg="white", command=lambda: pondre("ouvriere"))
    btn_eclaireuse = Button(frame_bas, text=" Pondre Éclaireuse ! (5 nectars) ", font=("Arial", 10,"bold" ),
                            bg="#2F1559", fg="white", command=lambda: pondre("eclaireuse"))
    btn_bourdon = Button(frame_bas, text=" Pondre Bourdon ! (5 nectars) ", font=("Arial", 10, "bold"), 
                        bg="#2F1559", fg="white", command=lambda: pondre("bourdon"))
    btn_passer = Button(frame_bas, text="   PASSER   ", font=("Arial", 12, "bold"), 
                       bg="#000000", fg="white", command=passer_phase)
    btn_passer.pack(side=TOP, pady=10)
    canvas.bind("<Button-1>", clic_plateau)
    redessiner()
    fenetre.mainloop()


def lancer_partie():
    """  
    Fonction pour lancer le jeu avec tous les settings par défaut
    """
    print("Lancement du jeu...") #Message d'alerte 
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs(NFLEURS)
    placer_fleurs(plateau, fleurs)
    
    afficher_plateau(plateau, ruches, 1)


if __name__ == "__main__":
    lancer_partie()
