#main.py comporte tout ce qui concerne l'affichage
from tkinter import *
from model import *

COULEURS_RUCHES = {
    "ruche0": "bleu",
    "ruche1": "rouge",
    "ruche2": "vert",
    "ruche3": "jaune"
}

TAILLE_SPRITE_ORIGINALE = 1024  # Change selon la taille des PNG

def charger_image(chemin, taille_case):
    """
    Charge une image et la redimensionne avec subsample
    """
    try:
        ratio = max(1, TAILLE_SPRITE_ORIGINALE // int(taille_case)) #de combien on rétréci
        image = PhotoImage(file=chemin).subsample(ratio, ratio)
        return image
    except:
        print(f"Attention : {chemin} introuvable")
        return None
    
def charger_abeille(role, camp, direction, taille_case):
    """
    Charge l'image d'une abeille selon son type, couleur et direction
    """
    couleur = COULEURS_RUCHES[camp]
    chemin = f"image/abeilles/{role}_{couleur}_{direction}.png"
    return charger_image(chemin, taille_case)

def charger_ruche(camp, taille_case):
    """
    Charge l'image d'une ruche selon sa couleur
    """
    couleur = COULEURS_RUCHES[camp]
    chemin = f"image/ruches/ruche_{couleur}.png"
    return charger_image(chemin, taille_case)

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
        canvas.create_line(0, i*taille_case, width, i*taille_case, fill="#000000", width=2)
        canvas.create_line(i*taille_case, 0, i*taille_case, height, fill="#000000", width=2)

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

def dessiner_plateau(canvas, plateau, taille_case, images_ruches, image_fleur, images_abeilles, image_terre):
    """
    Parcourt le plateau et dessine chaque élément avec la bonne image
    """
    if image_terre:
        for x in range(NCASES):
            for y in range(NCASES):
                # Vérifier si on est PAS dans une zone protégée (4x4 coins)
                dans_zone_protegee = (
                    (x < 4 and y < 4) or           # haut-gauche (ruche 0)
                    (x < 4 and y >= NCASES-4) or   # haut-droite (ruche 1)
                    (x >= NCASES-4 and y < 4) or   # bas-gauche (ruche 2)
                    (x >= NCASES-4 and y >= NCASES-4)  # bas-droite (ruche 3)
                )
                
                # Dessiner le terrain seulement si on est PAS dans une zone protégée
                if not dans_zone_protegee:
                    centre_x = y * taille_case + taille_case // 2
                    centre_y = x * taille_case + taille_case // 2
                    canvas.create_image(centre_x, centre_y, image=image_terre)

    for x in range(NCASES): #ligne
        for y in range(NCASES): #colonne
            case = plateau[x][y]  # Liste d'éléments
            
            # Parcourir tous les éléments dans LA CASE
            for element in case:
                if type(element) is dict: #Vérifier si c'est une liste ou un dict direct
                    if element["type"] == "ruche":
                        image = images_ruches.get(element["id"])
                        if image:
                            dessiner_ruche(canvas, x, y, taille_case, image)
                    elif element["type"] == "fleur":
                        if image_fleur:
                            dessiner_fleur(canvas, x, y, taille_case, image_fleur)
                    elif element["type"] == "abeille":
                        cle = f"{element['role']}_{element['camp']}_{element['direction']}"#clé : role_camp_direction
                        image = images_abeilles.get(cle)
                        if image:
                            dessiner_abeille(canvas, x, y, taille_case, image)

def afficher_plateau(plateau, ruches, tour_actuel, nectar_total_initial):
    """  
    Création de la fenêtre avec TOUT
    """
    fenetre = Tk() 
    fenetre.title("BZZZ - Guerre des nahlas") #titre de la fenêtre
    fenetre.geometry("1360x990")   # dimension de la fenetre
    fenetre.resizable(False, False)  # désactive agrandissement horizontal et vertical
    fenetre.configure(bg="#2C2C2C")  #fond 
    #Dimension
    width = 700
    height = width #carré
    taille_case = width / NCASES #nombre de pixel 

    #Chargement des images :
    print("Chargement des images..")
    #RUCHE :
    images_ruches = {}
    for ruche_id in COULEURS_RUCHES.keys(): #clé du dict couleurruche : ruche0, ruche1 etc..
        images_ruches[ruche_id] = charger_ruche(ruche_id, taille_case)
    #FLEUR :
    image_fleur = charger_image("image/fleur.png", taille_case)
    #BACKGROUND TERRAIN
    image_terre = charger_image("image/terre_seamless.png", taille_case)  
    #ABEILLE :
    images_abeilles = {}
    for role in ["bourdon", "ouvriere", "eclaireuse"]:
        for ruche_id in ["ruche0", "ruche1", "ruche2", "ruche3"]:
            for direction in ["droite", "gauche"]:
                cle = f"{role}_{ruche_id}_{direction}"
                images_abeilles[cle] = charger_abeille(role, ruche_id, direction, taille_case)
    
    print("Images chargées !")
    #Variable
    joueur_actuel = 0 #savoir qui joue
    phase = "ponte" #savoir à quel phase nous sommes
    abeille_cliquee = None #savoir qui est selectionné
    POSITIONS_RUCHES = {0: (0,0), 
                        1: (0,15), 
                        2: (15,0), 
                        3: (15,15)}
    #Interface
    
    label_tour = Label(fenetre, text="", font=("Arial", 18, "bold"),
                      bg="#1A1A1A", fg="#FFD700", pady=10)
    label_tour.grid(row=0, column=0, columnspan=3, sticky="ew")

    
    label_phase = Label(fenetre, text="", font=("Arial", 14, "bold"), 
                       bg="#4A90E2", fg="white", pady=8)
    label_phase.grid(row=1, column=0, columnspan=3, sticky="ew")
    
    #plateau centré
    
    canvas = Canvas(fenetre, width=width-1, height=height-1, bg="green",
                   highlightthickness=2, highlightbackground="#000000")
    canvas.grid(row=2, column=1, padx=10, pady=10)
    
    #Info ruches gauches
    frame_gauche = Frame(fenetre, width=270, bg="#2C2C2C")  
    frame_gauche.grid(row=2, column=0, sticky="ns", padx=10)

    # Ruche 0 (haut-gauche) en haut
    
    label_ruche0 = Label(frame_gauche, text="", bg="#87CEEB", font=("Arial", 11, "bold"), 
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#000080", anchor="n", justify="left", padx=8, pady=8)
    label_ruche0.pack(pady=12, padx=5, fill="both", expand=True)  

    # Ruche 2 (bas-gauche) en bas
    
    label_ruche2 = Label(frame_gauche, text="", bg="#90EE90", font=("Arial", 11, "bold"), 
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#006400", anchor="n", justify="left", padx=8, pady=8)
    label_ruche2.pack(pady=12, padx=5, fill="both", expand=True)  

    # Infos ruches droite (ruches du côté droit du plateau)
    frame_droite = Frame(fenetre, width=270, bg="#2C2C2C")  
    frame_droite.grid(row=2, column=2, sticky="ns", padx=10)

    # Ruche 1 (haut-droite) en haut
    
    label_ruche1 = Label(frame_droite, text="", bg="#FFB6C1", font=("Arial", 11, "bold"), 
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#8B0000", anchor="n", justify="left", padx=8, pady=8)
    label_ruche1.pack(pady=12, padx=5, fill="both", expand=True)  # ← MODIFIÉ : pady=12

    # Ruche 3 (bas-droite) en bas
    
    label_ruche3 = Label(frame_droite, text="", bg="#FFFF99", font=("Arial", 11, "bold"), 
                        width=28, height=13, relief="raised", borderwidth=3,
                        fg="#8B6914", anchor="n", justify="left", padx=8, pady=8)
    label_ruche3.pack(pady=12, padx=5, fill="both", expand=True)  # ← MODIFIÉ : pady=12

    labels_ruches = [label_ruche0, label_ruche1, label_ruche2, label_ruche3]

    #Frame pour boutons et message
    
    frame_bas = Frame(fenetre, height=120, bg="#2C2C2C")
    frame_bas.grid(row=3, column=0, columnspan=3, pady=5, sticky="ew")
    frame_bas.grid_propagate(False)  # ← NOUVEAU : Empêche le frame de changer de taille
    
    # Sous-frame pour les boutons de ponte
    frame_boutons_ponte = Frame(frame_bas, bg="#2C2C2C", height=50)
    frame_boutons_ponte.pack(side=TOP, pady=(5, 0))
    
    # Bouton PASSER 
    btn_passer = Button(frame_bas, text="PASSER LA PHASE", 
                       font=("Arial", 14, "bold"), 
                       bg="#FF6B35", fg="white", 
                       activebackground="#FF8C61", activeforeground="white",
                       width=30, height=2,
                       relief="raised", borderwidth=3,
                       cursor="hand2")
    btn_passer.pack(side=TOP, pady=(10, 5))
    
    #Nouveau style pour label_message
    label_message = Label(frame_bas, text="", font=("Arial", 11, "bold"), 
                         bg="#2C2C2C", fg="#00FF00", height=1)
    label_message.pack(side=TOP, pady=(0, 5))
    
    # Nouveau style pour label_gagnant
    label_gagnant = Label(fenetre, text="", font=("Arial", 20, "bold"), 
                         bg="#FFD700", fg="#8B0000", pady=5)
    label_gagnant.grid(row=4, column=0, columnspan=3, sticky="ew")
    
    #== FONCTIONS LOCALES ==
    def message(texte, couleur="red"):
        """  
        On donne un texte et sa couleur et ça converti en texte 
        qu'on peut voir sur le jeu
        """
        label_message.config(text=texte, fg=couleur)
        fenetre.after(2500, lambda: label_message.config(text=""))

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
        fini, gagnant, raison = fin_de_partie(plateau, ruches, tour_actuel, nectar_total_initial)
        if fini:
            messages_fin = {
                "timeout": f" Temps écoulé ! {gagnant['id']} GAGNE avec {gagnant['nectar']} nectar !",
                "blitzkrieg": f" VICTOIRE ÉCLAIR ! {gagnant['id']} GAGNE avec {gagnant['nectar']} nectar !",
                "epuisement": f" Plus de nectar ! {gagnant['id']} GAGNE avec {gagnant['nectar']} nectar !"
            }
            label_gagnant.config(text=messages_fin.get(raison, "FIN"))
            btn_passer.config(state="disabled")  # désactive le bouton passer en fin de partie
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
            message(erreur, "#FF4444")  
            return
        else:
            message(f"{type_abeille} viens de rejoindre cette guerre !", "#00FF00") 
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
                        message("Vous avez sélectionné cette abeille ! Cliquez où aller !", "#00BFFF")
                        redessiner()
                        return
            else:
                #mettre à jour la direction
                x_old, y_old = abeille_cliquee["position"]
                if y > y_old: #y = horizontale à cause de la structure du plateau(colonne)
                    abeille_cliquee["direction"] = "droite"
                elif y < y_old:
                    abeille_cliquee["direction"] = "gauche" 
                succes, erreur = tenter_deplacement(plateau, abeille_cliquee, (x,y), ruches)
                if erreur:
                    message(erreur, "#FF4444") 
                    return
                message("C'est bon il a bougé !", "#00FF00") 
                abeille_cliquee = None #reset
                redessiner()
                return
        elif phase == "butinage":
            for element in case:
                if (isinstance(element,dict) and
                    element.get("type") == "abeille" and
                    element["camp"] == ruche["id"] and
                    element["etat"] == "OK" and
                    element["a_bouge"] == False):
                    succes, resultat = tenter_butinage(plateau, element, ruche)
                    if succes == False:
                        message(resultat, "#FF4444")  
                        return
                    else:
                        message(f"Butiné ! +{resultat}", "#00FF00")  
                        redessiner()
                        return

    # ========== FONCTION REDESSINER ==========
    def redessiner():
        """  
        Permet de faire animé le plateau
        On supprime tout et on remet avec l'update :)
        """
        # Redessiner le plateau
        canvas.delete("all")
        dessiner_zones_protegees(canvas, taille_case, width, height)
        dessiner_plateau(canvas, plateau, taille_case, images_ruches, image_fleur, images_abeilles, image_terre)
        dessiner_quadrillage(canvas, width, height, taille_case)
        
       
        if abeille_cliquee:
            x, y = abeille_cliquee["position"]
            cx = y * taille_case + taille_case // 2
            cy = x * taille_case + taille_case // 2
            canvas.create_oval(cx-25, cy-25, cx+25, cy+25, outline="white", width=4)
            canvas.create_oval(cx-28, cy-28, cx+28, cy+28, outline="white", width=2)
        
        
        label_tour.config(text=f"TOUR {tour_actuel} / {TIME_OUT}")
        
        ruche = ruches[joueur_actuel]
        joueur_num = int(ruche['id'][-1]) + 1  
        
        
        if phase == "ponte":
            label_phase.config(
                text=f"JOUEUR {joueur_num} - PHASE DE PONTE",
                bg="#9B59B6", font=("Arial", 14, "bold")
            )
        elif phase == "mouvement":
            label_phase.config(
                text=f"JOUEUR {joueur_num} - PHASE DE MOUVEMENT",
                bg="#3498DB", font=("Arial", 14, "bold")
            )
        elif phase == "butinage":
            label_phase.config(
                text=f"JOUEUR {joueur_num} - PHASE DE BUTINAGE",
                bg="#27AE60", font=("Arial", 14, "bold")
            )
        elif phase == "escarmouche":
            label_phase.config(
                text=f"JOUEUR {joueur_num} - ESCARMOUCHE EN COURS...",
                bg="#E74C3C", font=("Arial", 14, "bold")
            )
        
        for widget in frame_boutons_ponte.winfo_children():
            widget.destroy()
            
        if phase == "ponte":
            # ← NOUVEAU : Créer les 3 boutons de ponte avec nouveau style
            btn_ouvriere = Button(frame_boutons_ponte, 
                                 text="OUVRIERE (5 nectars)", 
                                 font=("Arial", 12, "bold"),
                                 bg="#8E44AD", fg="white", 
                                 activebackground="#9B59B6",
                                 width=20, height=2,
                                 relief="raised", borderwidth=3,
                                 cursor="hand2",
                                 command=lambda: pondre("ouvriere"))
            btn_ouvriere.pack(side=LEFT, padx=8)
            
            btn_eclaireuse = Button(frame_boutons_ponte, 
                                   text="ECLAIREUSE (5 nectars)", 
                                   font=("Arial", 12, "bold"),
                                   bg="#3498DB", fg="white",
                                   activebackground="#5DADE2",
                                   width=20, height=2,
                                   relief="raised", borderwidth=3,
                                   cursor="hand2",
                                   command=lambda: pondre("eclaireuse"))
            btn_eclaireuse.pack(side=LEFT, padx=8)
            
            btn_bourdon = Button(frame_boutons_ponte, 
                                text="BOURDON (5 nectars)", 
                                font=("Arial", 12, "bold"),
                                bg="#E67E22", fg="white",
                                activebackground="#F39C12",
                                width=20, height=2,
                                relief="raised", borderwidth=3,
                                cursor="hand2",
                                command=lambda: pondre("bourdon"))
            btn_bourdon.pack(side=LEFT, padx=8)
        
        
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
            
            
            texte = f"JOUEUR {int(ruche['id'][-1])+1}\n\n"
            texte += f"Nectar: {ruche['nectar']}\n"
            texte += f"Abeilles actives: {nb_actives}\n"
            texte += f"Abeilles KO: {nb_ko}"

            # Mettre à jour le texte du label
            if i == joueur_actuel:
                
                label.config(text=f"{texte}\n\n>>> A TON TOUR <<<",
                           font=("Arial", 12, "bold"), 
                           relief="sunken", borderwidth=4)  
            else:
                label.config(text=texte,
                           font=("Arial", 11, "bold"),
                           relief="raised", borderwidth=3)
    
    btn_passer.config(command=passer_phase)
    
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

    nectar_total_initial = calculer_nectar_total_initial(plateau)

    afficher_plateau(plateau, ruches, 1, nectar_total_initial)


if __name__ == "__main__":
    lancer_partie()
