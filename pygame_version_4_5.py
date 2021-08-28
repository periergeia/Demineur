#possibilité de cacher le chrono avec un boutton
#texture règles pour affichage avec boutton in main menu
#trouver son pour clic et survolage bouttons

#importation des modules nécéssaires au programme
import pygame,random,time,tkinter,sys
import pygame.freetype










#définitions des variables du programme :

#de la longueur et de la largeur de la fenêtre de pygame
WINDOW_WIDTH = 832
WINDOW_HEIGHT = 572

#de différentes couleurs
COULEUR_BOUTTON = (145,145,182)
COULEUR_ENTRY = (152,152,186)
COULEUR_FOND = (167,169,190)
COULEUR_TEXTE_ERREUR = (215,34,50)
COULEUR_TEXT = (79,84,131)

#de dictionnaires pour respectivement les couleurs à utiliser selon la valeur de la case et les textes et/ou données
color = {'1':(182,216,157),'2':(157,216,200),'3':(157,188,216),'4':(185,167,218),'5':(216,171,156),'6':(216,191,158),'7':(223,223,150),'8':(203,217,156),"drapeau":(175,78,75),"bombe":(91,91,91),"win":(64,163,73),"lost":(197,30,31)}
text = {'1':["Félicitations !","Vous avez réussi à","déminer toutes les bombes"],'-1':["Perdu !","Vous avez marché","sur une bombe !","BOOM!"],'-2':["Perdu !","Triste, vous n\'avez","plus aucun drapeau"],"partie_personnalisée":{"colonne":{"text":"COLONNE(S)","x":180,"y":39},"ligne":{"text":"LIGNE(S)","x":394,"y":79},"bombe":{"text":"BOMBE(S)","x":608,"y":68}},"erreur_graine":["une graine est un nombre entier !","le contenu du presse-papier n'est pas elligible !"],"erreur_pp":["un nombre entier est attendu !","le nombre que vous essayez de choisir est trop grand !","saisissez le nombre de {} !","saisissez un nombre non nul !","le nombre de {} ne peut pas être plus petit !","pas plus de bombes que de cases :)"],"copy_seed":[[{"text":"appuyez sur la graine pour la","y":16},{"text":"copier afin de rejouer la partie !","y":36}],[{"text":"la graine a été copiée dans le","y":16},{"text":"clipboard (presse-papier)","y":36}]]}

#d'un booléen utile au jeu
game = False





#initialisation de modules :

#pygame, utilisé tout au long du programme
pygame.init()

#tkinter pour avoir accès au presse-papier, copier dans et obtenir la valeur stockée
tk = tkinter.Tk()
tk.withdraw()

#préréglage du module mixer
pygame.mixer.pre_init(44100,-16,2,1024)
pygame.mixer.music.set_volume(0.4)





#définition de la fenêtre pygame
fenêtre = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))





#importation :

#d'images
boutton = pygame.image.load("images/boutton.png").convert_alpha()
case_vide = pygame.image.load("images/vide.png").convert_alpha()
fond_menu_1 = pygame.image.load("images/fond_menu_principal.png").convert_alpha()
fond_menu_2 = pygame.image.load("images/fond_menu_difficulty.png").convert_alpha()
fond_menu_3 = pygame.image.load("images/fond_menu_graine.png").convert_alpha()
graine_erreur = pygame.image.load("images/graine_erreur.png").convert_alpha()
selected_case = pygame.image.load("images/selected_case.png").convert_alpha()
retour = pygame.image.load("images/retour.png").convert_alpha()
unselected_case = pygame.image.load("images/unselected_case.png").convert_alpha()

#de son
sfx_bang = pygame.mixer.Sound("son/bang.wav")

#de font
font0 = pygame.font.Font("Britannic.ttf", 16)
font1 = pygame.font.Font("Britannic.ttf", 20)
font2 = pygame.font.Font("Britannic.ttf", 30)
font3 = pygame.font.Font("Britannic.ttf", 40)
font_paramètres = pygame.freetype.Font("Britannic.ttf",30)
fontchrono = pygame.freetype.Font("Britannic.ttf", 35)
fontchrono.origin=True





#personnalisation de la fenêtre de jeu
pygame.display.set_caption("Jeu du démineur")
pygame.display.set_icon(unselected_case)










def création_button(position,texte,image_width,image_hight):

    '''Permet la création d'un boutton visible, une position sous forme d'un tuple de deux int (abcisse et ordonnée de la fenêtre pygame),
    et le texte à indiquer sur le boutton, l'image du boutton est définie par la largeur et la hauteur indiquées en paramètres.
    La fonction renvoie rect, une variable de type pygame.Rect, corrrespondant à la surface du boutton créé 

    >>> création_button((0,0),"Boutton1",70,90)'''
    
    #préparation du boutton visible au joueur
    w = font2.render(texte,1,COULEUR_TEXT).get_width()
    text = pygame.transform.scale(font2.render(texte,5,COULEUR_TEXT),(round(w*1.15),30))
    button = pygame.transform.scale(boutton,(image_width,image_hight))
    button.blit(text,(17,17))
    fenêtre.blit(button,position)

    #définition de la variable retournée
    rect = pygame.Rect(position[0],position[1],image_width,image_hight)

    return rect





def création_compteur(position_x,val_max,variable):

    '''Permet la création d'un 'compteur', une position à indiquer sous la forme d'un tuple de deux int,
    le compteur créé se présente tel trois bouttons, une, centrale se distingue des deux autres latérales par sa taille supérieures à ces dernières.
    La fonction retourne un tuple qui par la suite sera utilisée pour la création d'un dictionnaire.

    >>> création_compteurs((0,0),28,nb_colonnes)'''

    #création des bouttons utiles au compteur
    boutton_compteur = création_button((position_x,250),'',87,64)
    boutton_enlever = création_button((position_x-35,267),'',22,33)
    boutton_ajouter = création_button((position_x+101,267),'',22,33)
    rectgrey = pygame.Rect(position_x+6,257,77,48)

    return ("boutton_compteur",boutton_compteur),("rectgrey",rectgrey),("boutton_ajouter",boutton_ajouter),("boutton_enlever",boutton_enlever),("pos_x",position_x),("max",val_max),("valeur",variable)





def generate(nb_bombes,nb_lignes,nb_colonnes,seed=None):

    '''Permet de démarrer la génération d'un niveau avec le nombre de bombes définie (nb_bombes), le nombre de case sur l'axe X (nb_colonnes),
    le nombre de case sur l'axe Y (nb_lignes) et une graine (seed) qui à défaut sera choisie dans la fonction.
    la fonction retourne le tableau caché au joueur contenant les valeurs de la parties (hiddentableau), le numéro de la graine générée au hasard
    si non définie (seed), la liste contenant le placement des bombes de la partie (bombplacement) et le tableau visible par le 
    joueur durant la partie gameplay (showedtableau).
    Autrement, la fonction renvoie également limx, blockSize et rects des variables utiles pour la création du tableau graphique du jeu.
    limx correspond à la taille de la grille sur l'axe x, blockSize la taille d'une case et rect la liste contenant les éléments type pygame.Rects
    qui serviront par la suite à l'interaction avec le joueur. 

    >>> generate(5,10,10,-63486534658)'''
    
    #définition de variables
    #une liste permettant de vérifier les huit positionnements autour d'une bombe par une somme selon abscisse à abscisse et ordonnée à ordonnée
    sides = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    #définition de variables, respectivement : limite du tableau sur l'axe X, limite du tableau sur l'axe Y, variable permettant de déduire la taille d'une case et une liste vide pour contenir les cases du tableau de type pygame.Rect
    limx,limy,blockSize,rects = 575,WINDOW_HEIGHT,100000,[]


    #création des tableaux du jeu
    hiddentableau = [[0 for i in range(nb_colonnes)] for j in range(nb_lignes)]
    showedtableau = [[['◼',0] for i in range(nb_colonnes)] for j in range(nb_lignes)]


    #création de l'aléatoire à partir d'une seed
    if seed is None:
        seed = random.randint(-999999999999,1000000000000)
    random.seed(seed)


    #détermine le placement des différentes bombes en tenant en compte la taille du tableau de jeu
    bombplacement = []
    while nb_bombes != 0:
        xbomb = random.randint(0,nb_colonnes-1)
        ybomb = random.randint(0,nb_lignes-1)
        if (xbomb,ybomb) not in bombplacement:
            bombplacement.append((xbomb,ybomb))
            nb_bombes -= 1


    #place les bombes et les chiffres autour des bombes dans le tableau de jeu
    for k in bombplacement:
        hiddentableau[k[1]][k[0]] = '☢'
        for l in sides:
            testsidex, testsidey = k[0]+l[0],k[1]+l[1]
            try:
                if testsidex >= 0 and testsidey >= 0:
                    hiddentableau[testsidey][testsidex] += 1
                testsidex,testsidey = k[0],k[1]
            except:
                testsidex,testsidey = k[0],k[1]



    #déduction de la taille d'une seule case
    for i in range(100000):
        x = nb_colonnes*blockSize
        y = nb_lignes*blockSize
        if x>limx or y>limy:
            blockSize-=1
            continue
        break


    #remplissage de rects
    debut_x,debut_y = round((limx-blockSize*nb_colonnes)/2),round((limy-blockSize*nb_lignes)/2)
    for x1 in range(0, x, blockSize):
        rect_selected = []
        for y1 in range(0, y, blockSize):
            rect = pygame.Rect(y1+debut_y, x1+debut_x, blockSize, blockSize)
            rect_selected.append(rect)
        rects.append(rect_selected)
    
    return hiddentableau,seed,showedtableau,limx,blockSize,rects





def mis_a_jour_tableau(hiddentableau,showedtableau,ligne,colonne,drapeau):

    '''Permet de gérer les conséquences de l'action effectuée par le joueur sur le tableau et retourne la mise à jour du tableau visible
    par le joueur.

    >>> mis_a_jour_tableau([[0,0,0],[0,☢,0],[0,0,☢]],[[◼,◼,◼],[◼,◼,◼],[◼,◼,◼]],3,3,o)'''

    global nb_bombes,nb_drapeau,win

    #déclenchement de l'algorithme du remplacage des cases vide rempli par un caractère spécial pour montrer toute les cases vides lorsque le joueur clique sur une case vide
    if hiddentableau[int(colonne)-1][int(ligne)-1] == 0:
        replace_cases_vides(hiddentableau,showedtableau,0,['⛶',0])
    
        return showedtableau


    # Regarde si le joueur a placé un drapeau
    if drapeau == 'o':
        nb_drapeau -= 1
        # Si le drapeau a été placé sur une bombe :
        if hiddentableau[int(colonne)-1][int(ligne)-1] == '☢':
            # Enlève n-1 sur le nombre de bombes
            nb_bombes = int(nb_bombes)-1
            showedtableau[int(colonne)-1][int(ligne)-1][0] = '⚐'
            hiddentableau[int(colonne)-1][int(ligne)-1] = '⚐'
        else:
            showedtableau[int(colonne)-1][int(ligne)-1][0] = hiddentableau[int(colonne)-1][int(ligne)-1]
            hiddentableau[int(colonne)-1][int(ligne)-1] = hiddentableau[int(colonne)-1][int(ligne)-1]
        
        return showedtableau

    else:
        #attribue -1 à win qui signifie que la partie est perdue parce que le joueur a choisi une case contenant une bombe sans placer de drapeau
        if hiddentableau[int(colonne)-1][int(ligne)-1] == '☢':
            win = -1

            return showedtableau

        #autrement, place le chiffre de la case présente sur le tabelau caché sur le tableau visible au joueur
        else:
            showedtableau[int(colonne)-1][int(ligne)-1][0] = hiddentableau[int(colonne)-1][int(ligne)-1]

            return showedtableau





def replace_cases_vides(tableau1,tableau2,armplc,rmplcpar):

    '''Permet de remplacer sur le tableau visible au joueur par un caractère spécial les cases vides selon le tableau caché.

    >>> replace_cases_vides([[0,0,0],[0,☢,0],[0,0,☢]],[[◼,◼,◼],[◼,◼,◼],[◼,◼,◼])
    >>> REFAIRE L'EXEMPLE'''

    for i in range(len(tableau1)):
        for k in range(len(tableau1[i])):
            try:
                if tableau1[k][i][1] == armplc:
                    tableau2[k][i][1] = rmplcpar
            except:
                if tableau1[i][k] == armplc:
                    tableau2[i][k] = rmplcpar





def checkwin():

    '''Permet de vérifier si la partie est perdue ou bien gagnée au cours du jeu.
    
    >>> checkwin()'''

    global win,nb_drapeau,nb_bombes,hiddentableau,showedtableau,seed,xgrille,ygrille
    
    #si l'une des conditions de la partie perdue est vraie (lorsque le joueur a choisi une case contenant une bombe, la variable win vaut -1)
    if nb_drapeau == 0 or nb_bombes == 0 or win == -1:
        if win != -1:
    
            #le nombre de drapeau est nul tandis qu'il reste des bombes, win vaudra -2 pour signifier la perte par cette cause
            if int(nb_bombes) > 0:
                win = -2
    
            #la partie est gagnée, lorsque win vaudra 1, cela signifie que la partie est gagnée
            else:
                win = 1
        else:
    
            #joue de le son pour simuler l'explosion de la bombe
            sfx_bang.play()
        
        #met en place la fin d'une partie 
        replace_cases_vides(hiddentableau,showedtableau,0,['⛶',0])





def verif_quitter():

    '''Lorque le joueur clique sur la croix en haut à droite de la fenêtre, fait en sorte de quitter le jeu.

    >>> verif_quitter()'''

    global event
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()





def verif_retour_menu(booleen,boutton,affichage):

    '''A MODIFIER si le boutton Retour au menu est appuyé, permet de quitter la partie

    >>> verif_retour_menu()'''

    global event

    if affichage == True:
        fenêtre.blit(selected_case,(747,9))
        fenêtre.blit(retour,(747,9))
        pygame.display.flip()

    if boutton.collidepoint(pygame.mouse.get_pos()):
        booleen = False
    
    return booleen





def affichage(tableau,nb_drapeau,nb_bombes,seed):

    '''Permet d'afficher le tableau de jeu.
    
    >>> affichage(3,3,[[0,0,0],[0,☢,0],[0,0,☢]],4,-33243243)'''

    global menuquit,seedtext

    #affichage de ce qui se trouve à droite de la grille de jeu
    try:
        fenêtre.fill(0xA9A9C0)
        drapeautext = font2.render(f'Drapeau(x) : {str(nb_drapeau)}',1,COULEUR_TEXT)
        bombetext = font2.render(f'Bombe(s) : {str(nb_bombes)}',1,COULEUR_TEXT)
        seedtext = font0.render(f'Graine : {str(seed)}',1,COULEUR_TEXT)
        if seed is not None: fenêtre.blit(seedtext,(limx+7,395))
        w,h = seedtext.get_width(),seedtext.get_height()
        seedtext = pygame.Rect(limx+7,395,w,h)
        menuquit = création_button((limx+5,490),"Retour menu",WINDOW_WIDTH-limx-10,74)
        fenêtre.blit(drapeautext,(limx+7,315))
        fenêtre.blit(bombetext,(limx+7,355))


        #affiche le texte résultat de la partie lorsque la partie est finie
        if win != 0:
            if win == 1:
                result = "win"
            else:
                result = "lost"
            text_0 = font3.render(text[str(win)][0], 1, color[result])
            text_1 = font1.render(text[str(win)][1], 1, color[result])
            text_2 = font1.render(text[str(win)][2], 1, color[result])
            fenêtre.blit(text_0,(limx+7,100))
            fenêtre.blit(text_1,(limx+7,160))
            fenêtre.blit(text_2,(limx+7,180))
            try:
                text_3 = font3.render(text[str(win)][3], 1, color[result])
                fenêtre.blit(text_3,(limx+5,440))
            except: pass
    except: pass


    #placement des cases du jeu
    for i in range(xgrille):
        for k in range(ygrille):

            try:
                element = tableau[k][i][0]
            except:
                element = tableau[k][i]

            state = unselected_case
            try:
                if tableau[k][i][1] == 1:
                    state = selected_case
            except: pass

            if element == '◼':
                case_resize = pygame.transform.scale(state,(blockSize-1,blockSize-1))
                fenêtre.blit(case_resize, rects[i][k])
            elif element == 0 or element == '⛶':
                case_resize = pygame.transform.scale(case_vide,(blockSize-1,blockSize-1))
                fenêtre.blit(case_resize, rects[i][k])
            else :
                if element == '☢':
                    code = "bombe"
                elif element == '⚐':
                    code = "drapeau"
                else:
                    code = str(element)
                rect_x,rect_y,rect_w,rect_h = rects[i][k]
                pygame.draw.rect(fenêtre, color[code],(rect_x+round((rect_w-0.83*rect_w)/2),rect_y+round((rect_h-0.83*rect_h)/2),round(0.83*rect_w),round(0.83*rect_h)))
                case_resize = pygame.transform.scale(state, (blockSize-1, blockSize-1))
                fenêtre.blit(case_resize, rects[i][k])
                image_centre = pygame.image.load(f'images/{code}.png').convert_alpha()
                case_resize = pygame.transform.scale(image_centre, (blockSize-1, blockSize-1))
                fenêtre.blit(case_resize, rects[i][k])


    return rects





def affichage_message_erreur(menu,numéro_message,pos_x):

    '''Permet d'afficher le message d'erreur correspondant à l'erreur, le texte est contenu dans le dictionnaire text.
    
    >>> affichage_message_erreur("graine",1,40)'''

    global element

    #définition de quelques variables selon les données en argument de la fonction
    if menu == "graine":
        texte_erreur = text["erreur_graine"][numéro_message]
        fenêtre.blit(graine_erreur,(0,401))
        pos_y = 470
    elif menu == "partie_personnalisée":
        try:
            texte_erreur = text["erreur_pp"][numéro_message].format(element+'S')
        except:
            texte_erreur = text["erreur_pp"][numéro_message]
        pygame.draw.rect(fenêtre, COULEUR_FOND, pygame.Rect(0,500,WINDOW_WIDTH,75))
        pos_y = 517
    
    #affiche le message    
    message_erreur = font2.render(texte_erreur.upper(),1,COULEUR_TEXTE_ERREUR)
    fenêtre.blit(message_erreur,(pos_x,pos_y))
    




def menu_difficulty():

    '''Permet d'afficher et d'attendre la réponse du joueur sur le choix de la difficulté pour déterminer le niveau du jeu.
    
    >>> menu_difficulty()'''

    global difficulty,xgrille,ygrille,nb_bombes,event

    #affichage du menu des difficultés notamment avec la création de bouttons
    fenêtre.blit(fond_menu_2,(0,0))
    facile = création_button((170,260),"Facile . . . . . . . . . .",340,70)
    normal = création_button((170,330),"Normal . . . . . . . . . . . ." ,401,70)
    difficile = création_button((170,400),"Difficile . . . . . . . . . . . . . . .",462,70)
    expert = création_button((170,470),"Expert . . . . . . . . . . . . . . . . . . .",523,70)
    quitdifficulty = pygame.Rect(747,9,77,77)
    verif_retour_menu(difficulty,quitdifficulty,True)
    pygame.display.flip()


    #boucle attendant le choix du joueur, lorsqu'un boutton est cliqué, le nombre de bombes et le nombre de colonnes est définie en fonction de la difficulté choisie
    while difficulty:
        for event in pygame.event.get():
            verif_quitter()  
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                difficulty = verif_retour_menu(difficulty,quitdifficulty,True)
                try:

                    if facile.collidepoint(pygame.mouse.get_pos()):
                        nb_bombes,xgrille = 7,10

                    elif normal.collidepoint(pygame.mouse.get_pos()):
                        nb_bombes,xgrille = 20,15

                    elif difficile.collidepoint(pygame.mouse.get_pos()):
                        nb_bombes,xgrille = 55,17

                    elif expert.collidepoint(pygame.mouse.get_pos()):
                        nb_bombes,xgrille = 130,23

                except: pass


            if xgrille != None:
                #arrête la boucle et défini le nombre de lignes égal au nombre de colonnes
                difficulty = False
                ygrille = xgrille





def menu_graine():

    '''Permet d'afficher le menu pour définir la graine, la fonction attend que la graine saisie avec le clavier ou collée avec le raccourci "Ctrl+V"
    par le joueur soit validée avec un clic sur le boutton Continuer (créé avec la fonction) ou la touche Entrée du clavier.

    >>> menu_graine()'''
    
    global menugraine,graine_saisie,seed,event,difficulty,proceed

    #affichage du menu avec la création de bouttons
    fenêtre.blit(fond_menu_3,(0,0))
    fonct_entry,graine_saisie = False,''
    boutton_continuer = création_button((72,248),'',195,73)
    boutton_entry = création_button((263,248),graine_saisie,510,73)
    création_button((70,248),'',710,73)
    pygame.draw.line(fenêtre,COULEUR_TEXT,(265,253),(265,311),8)
    fenêtre.blit(font2.render("Continuer",1,COULEUR_TEXT),(100,267))
    fenêtre.blit(font3.render("Saisissez votre graine :)",1,COULEUR_TEXT),(302,100))

    quitgraine = pygame.Rect(747,9,77,77)
    proceed = False
    verif_retour_menu(menugraine,quitgraine,True)
    
    pygame.display.flip()
    

    #boucle principal de la fonction arrêtée lorsque le boutton Continuer est appuyé ou bien que la touche Entrée est enfoncée
    while menugraine:
        for event in pygame.event.get():
            verif_quitter()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                #vérifie si le boutton de retour est cliqué, si oui, change la valeur de la variable principale de la boucle while pour en sortir
                menugraine = verif_retour_menu(menugraine,quitgraine,True)
                
                #ferme la boucle lorsque le boutton Continuer est cliqué
                if boutton_continuer.collidepoint(pygame.mouse.get_pos()):
                    try:
                        if graine_saisie == '': seed = None
                        else : seed = int(graine_saisie)
                        proceed, menugraine = True, False
                    except:
                        pass

                #active l'entry lorsque le boutton de l'entry est pressé
                if boutton_entry.collidepoint(pygame.mouse.get_pos()):
                    fonct_entry = True
                else:
                    fonct_entry = False


            #lorsque l'entry est active après que le joueur ait appuyé sur le boutton
            if fonct_entry == True:
                rect_input = pygame.Rect(386,267,227,32)
                pygame.draw.rect(fenêtre,COULEUR_BOUTTON,rect_input)
                k_mod = pygame.key.get_mods()
                k_ = pygame.key.get_pressed()

                if event.type == pygame.KEYDOWN:
                    
                    #permet de saisir avec le clavier la graine en limitant les erreurs comme la saisie de caractères autre que chiffre
                    try:
                        int(event.unicode)
                        if graine_saisie == '' or graine_saisie == '-' or len(graine_saisie) < 13 and int(graine_saisie) <= 10**11-1:
                            graine_saisie += event.unicode
                            fenêtre.blit(graine_erreur,(0,401))
                    except:

                        #permet la saisie d'un nombre négatif
                        if event.unicode == '-'and graine_saisie == '':
                            graine_saisie += '-'
                        
                        #ignore l'appui sur la touche Shift pour que ce soit agréable (de ne pas voir de message d'erreur) lors de la saisie de chiffres
                        elif k_mod and pygame.KMOD_SHIFT:
                            pass
                        
                        #permet la supression d'un caractère en appuyant sur la touche Retour
                        elif k_[pygame.K_BACKSPACE]:
                            graine_saisie = graine_saisie[:-1]
                            fenêtre.blit(graine_erreur,(0,401))
                        
                        #la touche entrée permet de quitter la boucle principal, si rien n'est saisie la seed vaudra None, c'est comme si on avait ignoré le menu
                        elif k_[pygame.K_RETURN]:
                            if graine_saisie == '': seed = None
                            else : seed = int(graine_saisie)
                            proceed, menugraine = True, False
                        else :
                            affichage_message_erreur("graine",0,74)


                    #permet de coller la graine (avec un "Ctrl+V") copiée lors de la partie en limitant les erreurs
                    if k_mod and pygame.KMOD_CTRL:
                        if k_[pygame.K_v]:
                            try:
                                if int(tk.clipboard_get()) <= 10**12-1 :
                                    if len(tk.clipboard_get()) <= 13 :
                                        graine_saisie = tk.clipboard_get()
                            except:
                                affichage_message_erreur("graine",1,74)


                #met à jour ce que voit le joueur au fur et à mesure de sa saisie au clavier ou bien ce qui a été collé            
                text_surface = font2.render(graine_saisie,1,COULEUR_TEXT)
                fenêtre.blit(text_surface, (rect_input.x, rect_input.y))

            pygame.display.flip()
        
        #permet d'éviter que la boucle ne fonctionne trop vite et de se retrouver avec 22222222 pour avoir appuyé une fois sur la touche 2
        pygame.time.Clock().tick(60)





def menu_partie_personnalisée():

    '''Permet d'afficher le menu pour personnaliser la partie et d'attendre que le joueur ait choisi sa partie en définissant le nombre de colonnes,
    lignes et de bombes, la fonction est quittée lorsque le clic sur le boutton Continuer la partie est valable pour limiter les erreurs.

    >>> menu_partie_personnalisée'''

    global menupp,xgrille,ygrille,nb_bombes,seed,event,seed,element,proceed

    #affichage du menu ainsi que la création d'un dictionnnaire utilisé tout au long de la fonction, conteneur
    fenêtre.fill(0xA9A9C0)
    conteneur,clef_dico = {},["colonne","ligne","bombe"]
    conteneur["colonne"] = dict(création_compteur(158,28,10))
    conteneur["ligne"] = dict(création_compteur(372,28,10))
    conteneur["bombe"] = dict(création_compteur(586,784,7))
    boutton_result = création_button((123,410),"Commencer la partie . . . . . . . . . . .",585,74)

    quitpp = pygame.Rect(747,9,77,77)
    proceed = False
    verif_retour_menu(menupp,quitpp,True)

    
    #placement des textes de description des compteurs sur la fenêtre, et ce que les valeurs de chacun des compteurs de sorte à ce qu'ils soient centrés sur le boutton
    for e in clef_dico:
        conteneur[e][e] = False
        texte = pygame.transform.rotate(font2.render(text["partie_personnalisée"][e]["text"],1,COULEUR_TEXT), 90)
        w = font2.render(str(conteneur[e]["valeur"]),1,(0,0,0)).get_width()
        conteneur[e]["position"] = round((87-w)/2+conteneur[e]["pos_x"])
        fenêtre.blit(texte,(text["partie_personnalisée"][e]["x"],text["partie_personnalisée"][e]["y"]))
        font_paramètres.render_to(fenêtre,((conteneur[e]["position"]),267), str(conteneur[e]["valeur"]),COULEUR_TEXT)

    pygame.display.flip()
    

    #boucle principal de la fonction qui attend que le joueur se soit décidé sur les nombres de colonnes, lignes et bombes de la partie en pressant sur le boutton Continuer
    while menupp:
        for event in pygame.event.get():
            verif_quitter()
            for element in clef_dico:

                #permet de mettre à jour le nombre de bombes maximum permis lors de la partie et de réduire le nombre de bombes si le nombre de lignes ou de colonnes est insuffisant
                try:
                    conteneur["bombe"]["max"] = conteneur["colonne"]["valeur"]*conteneur["ligne"]["valeur"]
                    if conteneur["bombe"]["valeur"] > conteneur["bombe"]["max"]:
                        conteneur["bombe"]["valeur"] = round(conteneur["bombe"]["max"]/2)
                except:
                    if conteneur[element]["valeur"] != '':
                        affichage_message_erreur("partie_personnalisée",5,20)


                #lorsqu'une entry est active voir plus bas dans le code pour l'activation d'une entry :)                                                
                if conteneur[element][element] == True:
                    #prépare l'entry en dessinant un rectangle sur l'entry active et récupère dans les event pygame les touches pressées dans des variables
                    pygame.draw.rect(fenêtre,COULEUR_BOUTTON,conteneur[element]["rectgrey"])
                    k_mod = pygame.key.get_mods()
                    k_ = pygame.key.get_pressed()

                    if event.type == pygame.KEYDOWN:

                        #permet la saisie d'un nombre en limitant les erreurs, lorsqu'il y en a une, on fait afficher l'erreur avec la fonction affichage_message_erreur
                        try:
                            int(event.unicode)
                            if conteneur[element]["valeur"] == '' :
                                conteneur[element]["valeur"] = int(event.unicode)                          
                            elif conteneur[element]["valeur"]*10+int(event.unicode) <= conteneur[element]["max"]:
                                conteneur[element]["valeur"] = conteneur[element]["valeur"]*10+int(event.unicode)
                                pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(0,500,WINDOW_WIDTH,75))
                            else:
                                affichage_message_erreur("partie_personnalisée",1,8)                            
                        except:
                            
                            #ignore la touche Shift du clavier
                            if k_mod and pygame.KMOD_SHIFT: pass
                            
                            #permet de supprimer le dernier caractère saisie
                            elif k_[pygame.K_BACKSPACE]:
                                if conteneur[element]["valeur"] == '': pass
                                else :
                                    conteneur[element]["valeur"] = conteneur[element]["valeur"]//10
                                    pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(0,500,WINDOW_WIDTH,75))

                            #permet de désactiver l'entry si la valeur saisie est correcte (ça se fait aussi avec un clic sur un autre endroit que l'entry, hein :))
                            elif k_[pygame.K_RETURN]:
                                
                                #permet d'"effacer" le message d'erreur si la saisie est correcte
                                try:
                                    generate(conteneur["bombe"]["valeur"],conteneur["colonne"]["valeur"],conteneur["ligne"]["valeur"],seed)
                                    if conteneur["bombe"]["valeur"] <= conteneur["bombe"]["max"]:
                                        pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(0,500,WINDOW_WIDTH,75))
                                except: pass
                                
                                #permet d'indiquer au joueur de saisir une valeur puisque vide
                                if conteneur[element]["valeur"] == '' :
                                    affichage_message_erreur("partie_personnalisée",2,20)
                                
                                #la valeur de chacune des compteurs ne peut être égal à 0 (sauf pour le nombre de bombes ^^)
                                elif conteneur[element]["valeur"] == 0:
                                    affichage_message_erreur("partie_personnalisée",3,20)
                                    conteneur[element]["valeur"] = 1
                                
                                #si la valeur est bonne, "ferme" l'entry
                                else:
                                    conteneur[element][element] = False
                            else :
                                affichage_message_erreur("partie_personnalisée",0,20)


                    #affiche la mise à jour des valeurs
                    w = font2.render(str(conteneur[element]["valeur"]),1,(0,0,0)).get_width()
                    conteneur[element]["position"] = (87-w)/2+conteneur[element]["pos_x"]
                    pygame.draw.rect(fenêtre,COULEUR_ENTRY,conteneur[element]["rectgrey"])
                    font_paramètres.render_to(fenêtre,(round(conteneur[element]["position"]),267),str(conteneur[element]["valeur"]),COULEUR_TEXT)



                #c'est ici que la boucle vérifie si un boutton est cliqué
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                    #vérifie si le boutton de retour est cliqué, si oui, change la valeur de la variable principale de la boucle while pour en sortir
                    menupp = verif_retour_menu(menupp,quitpp,True)
                    
                    #si la génération d'une partie est permise avec les valeurs des différents compteurs, lorsque le boutton Continuer est appuyé, le menu peut être fermé
                    if boutton_result.collidepoint(pygame.mouse.get_pos()):
                        try:
                            generate(conteneur["bombe"]["valeur"],conteneur["colonne"]["valeur"],conteneur["ligne"]["valeur"],seed)
                            if conteneur["bombe"]["valeur"] <= conteneur["bombe"]["max"]:
                                proceed, menupp = True, False
                        except: pass
                    
                    #si le petit boutton à droite d'un compteur est appuyé, si l'ajout est permise, la valeur du compteur est augmenté de 1
                    if conteneur[element]["boutton_ajouter"].collidepoint(pygame.mouse.get_pos()):
                        try:
                            if conteneur[element]["valeur"] < conteneur[element]["max"]:
                                conteneur[element]["valeur"] += 1
                                pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(0,500,WINDOW_WIDTH,75))
                            elif conteneur[element]["valeur"] == conteneur[element]["max"]:
                                affichage_message_erreur("partie_personnalisée",1,8)
                        except:
                            conteneur[element]["valeur"] = 1
                            pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(0,500,WINDOW_WIDTH,75))

                    #si le petit boutton à gauche d'un compteur est appuyé et si la soustraction est permise, la valeur du compteur est diminué de 1
                    elif conteneur[element]["boutton_enlever"].collidepoint(pygame.mouse.get_pos()):
                        try:
                            if conteneur[element]["valeur"] > 1 :
                                pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(0,500,WINDOW_WIDTH,75))
                                conteneur[element]["valeur"] -= 1
                            else:
                                affichage_message_erreur("partie_personnalisée",4,8)
                        except:
                            affichage_message_erreur("partie_personnalisée",2,8)

                    #on met à jour les valeurs des compteurs
                    w = font2.render(str(conteneur[element]["valeur"]),1,(0,0,0)).get_width()
                    conteneur[element]["position"] = round((87-w)/2+conteneur[element]["pos_x"])
                    pygame.draw.rect(fenêtre,COULEUR_BOUTTON,conteneur[element]["rectgrey"])
                    font_paramètres.render_to(fenêtre,(conteneur[element]["position"],267),str(conteneur[element]["valeur"]),COULEUR_TEXT)

                    #si le boutton central du compteur (le boutton où la valeur du compteur est affichée) est appuyé, on active l'entry correspondant au compteur, autrement on le désactive
                    if conteneur[element]["boutton_compteur"].collidepoint(pygame.mouse.get_pos()):
                        conteneur[element][element],conteneur[element]["valeur"] = True,''
                    else:
                        conteneur[element][element] = False
                pygame.display.flip()
        
    
        #permet au programme de ne pas fonctionner trop vite
        pygame.time.Clock().tick(60)
    
    
    #on attribue les valeurs du dictionnaires à des variables pour la génération des tableaux du jeu
    ygrille,xgrille,nb_bombes = conteneur["colonne"]["valeur"],conteneur["ligne"]["valeur"],conteneur["bombe"]["valeur"]





def mainmenus():
    
    '''Permet l'affichage des menus disponibles au joueur et attend le choix de celui-ci sur la partie qu'il souhaite.

    >>> mainmenus()'''

    global game,difficulty,menugraine,menupp,seed,showedtableau,hiddentableau,xgrille,ygrille,nb_bombes,nb_drapeau,event,limx,blockSize,rects,proceed

    #affichage du menu avec la création des bouttons
    fenêtre.blit(fond_menu_1,(0,0))
    choix_partie_aléatoire = création_button((170,260),"Jouer à une partie aléatoire",468,74)
    choix_partie_graine = création_button((170,348),"Jouer en utilisant une graine",495,74)
    choix_partie_personnalisée = création_button((170,436),"Jouer une partie personnalisée",522,74)
    pygame.display.flip()


    #le menu attend un clic sur un boutton et appelle la fonction correspondante au choix du joueur, eventuellement une seconde s'il faut
    for event in pygame.event.get():
        verif_quitter()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                #lorsque le joueur choisi le menu des difficultés
            if choix_partie_aléatoire.collidepoint(pygame.mouse.get_pos()):
                difficulty,seed = True,None
                menu_difficulty()

            #lorsque le joueur choisi le menu graine
            elif choix_partie_graine.collidepoint(pygame.mouse.get_pos()):
                menugraine,difficulty,seed = True,True,None
                menu_graine()
                if proceed:
                    menu_difficulty()

            #lorsque le joueur choisi le menu d'une partie personnaliser
            elif choix_partie_personnalisée.collidepoint(pygame.mouse.get_pos()):
                menupp,menugraine,seed = True,True,None
                menu_partie_personnalisée()
                if proceed:
                    menu_graine()


    #génération des tableaux du jeu en fonctions des choix du joueur
    try:
        if proceed == True:
            nb_drapeau = round(nb_bombes*1.2)
            hiddentableau,seed,showedtableau,limx,blockSize,rects = generate(nb_bombes,ygrille,xgrille,seed)
            game = True
    except:
        pass





def chrono(ticks):
    
    '''Permet l'affichage du chrono lors de la partie. La variable ticks est générée par le module time.
    Elle renvoie les valeurs en durée du nombre d'heures, de minutes et de secondes de la partie.
    
    >>> chrono(1.3551149368286133)'''
    
    #création d'un rectangle afin que le chronomètre à afficher soit "propre" 
    rectgray = pygame.Rect(710, 437, 107, 33)
    pygame.draw.rect(fenêtre, COULEUR_FOND, rectgray)
    
    #calcule le nombre de secondes, de minutes et d'heures, stockées dans des variables
    seconds = int(ticks % 60)
    minutes = int(ticks/60 % 60)
    hours = int(ticks/3600 % 24)
    
    #évalue si l'affichage du nombre d'heure est nécéssaire 
    if hours >= 1:
        out='{h:02d}:{m:02d}:{s:02d}'.format(h=hours, m=minutes, s=seconds)
    else:
        out='{m:02d}:{s:02d}'.format(m=minutes, s=seconds)
    
    #affichage sur la fenêtre
    fontchrono.render_to(fenêtre, (720, 470), out, COULEUR_TEXT)

    return hours,minutes,seconds





def découverte_fin():
    
    '''Permet d'affcher le chronomètre arrêté, un message si la graine n'a pas été copiée ainsi que le tableau découvert à la fin de la partie.
    
    >>> découverte_fin()'''

    global rects

    # Copie le tableau caché avec toute les réponses sur le tableau que le joueur voit et affiche le tableau
    showedtableau = hiddentableau
    rects = affichage(showedtableau,nb_drapeau,nb_bombes,seed)

    #si la graine n'a pas été copiée, un message pour conseiller le joueur de la copier est affiché
    if copy == False :
        pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(578,15,243,41))
        for element in text["copy_seed"][0]:
            info = font0.render(element["text"],1,COULEUR_TEXT)
            fenêtre.blit(info,(582,element["y"]))

        #reaffiche le chrono de fin
        chrono(round(finalvalue))





def player_choice():
    
    '''Permet de prendre en compte les choix de cases et de placement de drapeau ou non du joueur lors de la partie par la vérification, elle permet entre
    autre d'afficher de démarrer le chrono et de l'afficher par la fonction chrono, vérifiant également que le statut copié ou non de la graine, affichant un message
    en fin de partie si celle-ci ne l'est pas, et un autre pour indiquer qu'elle l'est.
    
    >>> player_choice'''

    global game,nb_bombes,nb_drapeau,hiddentableau,showedtableau,seed,seedtext,win,event,rects,copy,finalvalue
    
    #initialisation de variables et affichage du tableau de jeu
    starttime,time_chrono,copy = time.time(),True,False
    rects = affichage(showedtableau,nb_drapeau,nb_bombes,seed)
    limite = pygame.Rect(rects[0][0].x,rects[0][0].y,ygrille*blockSize,xgrille*blockSize)
    pygame.display.flip()

    #boucle principale de la fonction, valable du moment que le joueur ne clique pas sur le boutton Retour au menu, ou qu'il ne choisisse pas de quitter la fenêtre
    while game:
        
        #permet l'évaluation et l'affichage du chronomètre dans la partie
        if time_chrono == True:
            ticks = time.time()
            ticksvalue = ticks - starttime
            chrono(round(ticksvalue))


        for event in pygame.event.get():
            verif_quitter()
            if event.type == pygame.MOUSEBUTTONUP:
                
                #vérifie si le joueur souhaite quitter la partie
                game = verif_retour_menu(game,menuquit,False)
    
                #permet de copier la valeur de la graine dans le presse_papier et d'activer une variable utilisée plus bas dans la fonction
                if seedtext.collidepoint(pygame.mouse.get_pos()):
                    tk.clipboard_clear()
                    tk.clipboard_append(seed)
                    copy = True

                #du moment que la partie n'est ni perdue ni gagnée
                if win == 0:
                    #parcourt la liste contenant les case de type pygame.Rect et vérifie si un drapeau est placée sur la case appuyée en prenant en compte le clic
                    for i in range(len(rects)):
                        for k in range(len(rects[i])):
                            if rects[i][k].collidepoint(pygame.mouse.get_pos()):
                                #clic droit, un drapeau est placé
                                if event.button == 3:
                                    drapeau = 'o'
                                #clic gauche, pas de drapeau
                                elif event.button == 1:
                                    drapeau = 'n'
                                
                                #affichage du tabelau mis à jour
                                showedtableau = mis_a_jour_tableau(hiddentableau,showedtableau,i+1,k+1,drapeau)
                                rects = affichage(showedtableau,nb_drapeau,nb_bombes,seed)
                                checkwin()


            if event.type == pygame.MOUSEMOTION and win == 0: ##dans le tableau de jeu condition
                for i in range(xgrille):
                    for k in range(ygrille):
                        if rects[i][k].collidepoint(pygame.mouse.get_pos()):
                            if showedtableau[k][i][1] == 1:
                                pass
                            else:
                                replace_cases_vides(showedtableau,showedtableau,1,0)
                                showedtableau[k][i][1] = 1
                                rects = affichage(showedtableau,nb_drapeau,nb_bombes,seed)
                                chrono(round(ticksvalue))
                        else:
                            if showedtableau[k][i][1] != 0:
                                showedtableau[k][i][1] = 0
                                if not limite.collidepoint(pygame.mouse.get_pos()):
                                    rects = affichage(showedtableau,nb_drapeau,nb_bombes,seed)
                                    chrono(round(ticksvalue))
                    
                        


        #lorsque la partie n'est plus en cours
        if win != 0 :

            #définition de variable pour stocker la valeur du chronomètre à la fin de la partie et d'arrêter celui-ci avec la variable time_chrono valant False
            finalvalue,time_chrono = ticksvalue,False

            #timestop correspond à la variable contenant le moment où la suite du programme peut être effectif pour l'attente durant l'animation, sous forme de liste pour une comparaison   
            timestop = list(chrono(finalvalue))
            if timestop[2]+3 < 60:
                timestop = [timestop[0],timestop[1],timestop[2]+3]
            else:
                if timestop[1]+1 < 59:
                    timestop = [timestop[0],timestop[1]+1,3-(60-timestop[2])]
                else:
                    timestop = [timestop[0]+1,0,3-(60-timestop[2])]


            if win == -1:

                #préparation de l'animation dans le cas où le joueur appuie sur une bombe et définition de tickscontinue qui est une sorte de chronomètre non visible au joueur
                tickscontinue = list(chrono(round(time.time()-starttime)))
                w,h = WINDOW_WIDTH,WINDOW_HEIGHT
                pos_x,pos_y = 0,0
                explosion = pygame.image.load("images/explosion.png").convert_alpha()

                #affichage une fois que tickscontinue vaudra timestop, signifiant que trois secondes serait passé entre le moment où la partie est terminée et le moment où cette inégalité sera vrai
                while tickscontinue <= timestop:
                    
                    #animation de l'explosion de la bombe, pygame.transform.scale gâche la résolution de l'image par contre  :/ (si,si allez vérifier l'image originale à son emplacement !)
                    
                    #affichage d'une image de l'animation
                    fenêtre.fill(0xCCCCCC)
                    fenêtre.blit(explosion,(round(pos_x),round(pos_y)))
                    pygame.display.flip()

                    #redéfinition de variables pour donner l'impression d'une expansion
                    explosion = pygame.transform.scale(explosion, (w,h))
                    pos_x,pos_y = pos_x-(round(w*1.035)-w)/2,pos_y-((round(h*1.035)-h))/2
                    w,h = round(w*1.035),round(h*1.035)
                    
                    #le chronomètre vaut toujours
                    tickscontinue = list(chrono(round(time.time()-starttime)))

                découverte_fin()

            #la même chose sans l'animation, la partie ne se solde pas par la défaite par explosion d'une bombe
            else:
                découverte_fin()


        #si la graine est copiée (lorsque le joueur appuie sur la graine, voir plus haut) 
        if copy == True:
            try:

                #permet de dissimuler l'état copié de la graine durant l'animation (pour un animation uniforme) puis affiche le message ainsi que reaffiche le chrono
                if tickscontinue > timestop:
                    pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(578,15,243,41))
                    for element in text["copy_seed"][1]:
                        info = font0.render(element["text"],1,COULEUR_TEXT)
                        fenêtre.blit(info,(582,element["y"]))
                    chrono(round(finalvalue))
            except:

                #affiche le message pour signifier que la graine a été copiée
                pygame.draw.rect(fenêtre,COULEUR_FOND,pygame.Rect(578,15,243,41))
                for element in text["copy_seed"][1]:
                    info = font0.render(element["text"],1,COULEUR_TEXT)
                    fenêtre.blit(info,(582,element["y"]))
                try: chrono(round(finalvalue))
                except : pass

        pygame.display.flip()










#boucle principale du jeu appelant une fonction (qui en appelle d'autres) selon si une partie est commencée ou non
while True:

    #la partie n'est pas commencée, appel de la fonction pour le menu principal
    if game == False:
        xgrille, ygrille, nb_bombes, seed = None, None, None, None
        mainmenus()

    #la partie est commencée, les paramètres du jeu sont choisis (dans la partie des menus), le joueur peut commencer à jouer avec la fonction
    if game == True:

        #initialise win, lorsqu'elle vaut 0, la partie n'est ni remportée ni perdue
        win = 0
        player_choice()