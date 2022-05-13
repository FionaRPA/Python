from upemtk import *
from random import randint
import os
import time
import copy

def coin_bas(i, j, k, lb, hb):
    """
    Cette fonction calcule les coordonnées, en pixels, du coin le plus bas 
    d'un bloc représenté par le triplet (i, j, k), où i est le numéro de 
    ligne et j le numéro de colonne de la case sur laquelle est posé le bloc, 
    et k est sa hauteur. Elle reçoit également les dimensions lb et hb d'un 
    bloc. 
    """
    x = (taille_x//2) + (j-i) * lb
    y = (taille_y//2) + (j+i) * lb//2 - (k-1) * hb + lb
    return x, y


def affiche_bloc(i, j, k, lb, hb, couleur = "darkblue"):
    """
    Cette fonction affiche le bloc de coordonnées (i, j, k) conformément au 
    schéma donné dans le sujet. Elle reçoit également les dimensions lb et hb 
    d'un bloc, la taille n du plateau ainsi qu'un paramètre optionnel c 
    indiquant la couleur de la face supérieure du bloc. 
    """
    # calcul des coordonnées du coin bas du bloc
    x, y = coin_bas(i, j, k, lb, hb)
    # calcul des coordonnées des autres sommets inférieurs du bloc
    xg, xd, ymb = x - lb, x + lb, y - lb//2
    # calcul des ordonnées des sommets supérieurs
    ybh, ymh, yhh = y - hb, y - lb//2 - hb, y - lb - hb

    # dessin de la face supérieure, en vert si c'est l'arrivée
    face_haut = [(x, ybh), (xd, ymh), (x,  yhh), (xg, ymh)]
    polygone(face_haut, remplissage = couleur, epaisseur = 2)

    # dessin des faces latérales si hauteur non nulle
    if k > 0:
        face_gauche = [(x, y),   (xg, ymb), (xg, ymh), (x,  ybh)]
        face_droite = [(x, y),   (xd, ymb), (xd, ymh), (x,  ybh)]
        polygone(face_gauche, remplissage='snow')
        polygone(face_droite, remplissage='lightgrey')


def affiche_bille(i, j, k, lb, hb, n):
    """
    Cette fonction affiche la bille aux coordonnées (i, j, k). Elle reçoit 
    également les dimensions lb et hb d'un bloc ainsi que la taille n du 
    plateau. 
    """
    # dessin de la bille proprement dite
    x, y = coin_bas(i, j, k, lb, hb)
    cercle(x, y - 2*lb//3, lb//3, couleur='firebrick', remplissage='firebrick')

    # repère vertical pour une meilleure visibilité
    ligne(x, y - 2*lb//3, x, 60, couleur='firebrick', epaisseur = 2)

    # flèche-repère de gauche
    x, y = coin_bas(n-1, j-0.5, 1, lb, hb)
    fleche(x - 20, y + 20, x - 10, y + 10,
           couleur= 'firebrick', epaisseur=3)

    # flèche-repère de droite
    x, y = coin_bas(i-0.5, n-1, 1, lb, hb)
    fleche(x + 20, y + 20, x + 10, y + 10,
           couleur='firebrick', epaisseur=3)


def affiche_texte() :
    """
    Cette fonction affiche tout le texte que l'on souhaite dire 
    avant de commencer le jeu. Puis, on l'efface à l'aide de la fonction 
    "efface_tout()"
    """    
    longueur = (taille_y/2) -50
    largeur = (taille_x/2) - 150
    rectangle(0, 0, taille_x, taille_y,  'white', 'white')
    texte(largeur, longueur, 'Pushit Game !', 'darkblue', taille = 35, police = 'Garamond')
    # On attend un clique pour ensuite effacer le texte
    attente_clic()
    efface_tout()
    # Afficher un autre texte qui sera effacer lui aussi
    largeur = (taille_x/2) - 300
    rectangle(0, 0, taille_x, taille_y,  'white', 'white')
    texte(largeur, longueur, 'Cliquer pour commencer le jeu', 'darkblue', taille = 28, police = "Garamond")
    attente_clic()
    efface_tout()


def affiche_texte_bis() :
    # Affiche le fond en blanc
    rectangle(0, 0, taille_x, taille_y,  'white', 'white')
    # Affichage du repère pour les flèches
    image(10,10,'fleche',ancrage='nw')
    largeur = taille_x - 150
    texte(largeur, 10, 'R : Retry\nN : Next\nP : Previous\nA : Annuler\nQ : Quit', 'darkblue', taille = 16, police = 'Garamond')


def affiche_menu() :
    rectangle(0, 0, taille_x, taille_y,  'white', 'white')
    texte(300, 20, 'Selectionnez un niveau:', 'blue', taille=20, police='Garamond')
    texte(350, 150, 'Niveau Facile', 'darkblue', taille=22, police='Garamond')
    ligne(0,(taille_y/3),taille_x,(taille_y/3),epaisseur=3,couleur='blue')
    texte(350, 450, 'Niveau Moyen', 'darkblue', taille=22, police='Garamond')
    ligne(0,(2*(taille_y/3)),taille_x,(2*(taille_y/3)),epaisseur=3,couleur='blue')
    texte(350, 750, 'Niveau Difficile', 'darkblue', taille=22, police='Garamond')


def menu():
    """
    Cette fonction affiche le menu où les différents niveau sont affichés. Le 
    joueur devra cliquer sur le niveau de difficulté qu'il souhaite.
    """
    affiche_menu()
    while True :
        evenement = donne_evenement()
        type_ev = type_evenement(evenement)
        if type_ev == 'ClicGauche' :
            if 30 < clic_y(evenement) < (taille_y/3) :
                return 'facile'
            elif (taille_y/3) < clic_y(evenement) < (2*(taille_y/3)) :
                return 'moyen'
            elif (2*(taille_y/3)) < clic_y(evenement) < taille_y :
                return 'difficile'
        mise_a_jour()


def liste_aleatoire(Bloc_aleatoire = []):
    """
    Cette fonction crée une liste de liste aléatoire qui servira pour le solver.
    """
    Sous_aleatoire = []
    nbre = randint(2,8)
    for cmpt in range(nbre) :
        Sous_aleatoire.append(randint(0,nbre))
    Bloc_aleatoire.append(Sous_aleatoire)
    if len(Bloc_aleatoire) == len(Sous_aleatoire) :
        return Bloc_aleatoire
    return liste_aleatoire(Bloc_aleatoire)


def liste_affiche(niveau, Bloc = [], hauteurmax = 0) :
    """
    Cette fonction affiche la liste de liste, qui est le niveau créer 
    à l'aide du fichier que l'on a ouvert auparavant. On lit 
    le fichier ligne par ligne. Puis on retourne la liste crée avec 
    la hauteur maximale des blocs c'est-à-dire le plus grand chiffres 
    de cette liste de liste.
    """
    niv = niveau.readline()
    SousBloc = []
    for cmpt in range(len(niv)) :
        # On ajoute pas dans notre liste les espaces et les sauts de lignes
        if niv[cmpt] == '\n' or niv[cmpt] == ' ' :
            pass
        # On ajoute les chiffres dans notre sous liste.
        else:
            SousBloc.append(int(niv[cmpt]))
            # On cherche la hauteur maximale en observant s'il y a un chiffre plus grand que les autres.
            if (int(niv[cmpt])) > hauteurmax :
                hauteurmax = (int(niv[cmpt]))
    # Puis, on ajoute cette sous liste dans notre liste principale.
    Bloc.append(SousBloc)
    if len(Bloc) == len(SousBloc) :
        return Bloc, hauteurmax
    # Avec la récursivité on retourne la fonction pour qu'elle parcour toute la liste.
    return liste_affiche(niveau, Bloc, hauteurmax)


def bloc_affiche(lb, hb, n, i, j, bloc) :
    """
    Cette fonction affiche les blocs "dans la fenêtre, comme le fait 
    la fonction "affiche_bloc" mais cette fonction affiche tout les 
    blocs possible.
    """
    for cmpt in range(n) :
        for cmpt1 in range(n) :
            if i == cmpt and j == cmpt1 :
                if bloc[cmpt][cmpt1] > 0 :
                    for c in range(bloc[cmpt][cmpt1]) :
                        affiche_bloc(cmpt, cmpt1, c, lb, hb)
                affiche_bloc(cmpt, cmpt1, bloc[cmpt][cmpt1], lb, hb, couleur = "lightgrey")
                affiche_bille(i, j, bloc[i][j] + 1, lb, hb, n)

            elif cmpt == (n - 1) and cmpt1 == (n - 1) :
                if bloc[cmpt][cmpt1] > 0 :
                    for c in range(bloc[cmpt][cmpt1]) :
                        affiche_bloc(cmpt, cmpt1, c, lb, hb)
                affiche_bloc(cmpt, cmpt1, bloc[cmpt][cmpt1], lb, hb, couleur = "firebrick")

            else :
                if bloc[cmpt][cmpt1] > 0 :
                    for c in range(bloc[cmpt][cmpt1]) :
                        affiche_bloc(cmpt, cmpt1, c, lb, hb)
                affiche_bloc(cmpt, cmpt1, bloc[cmpt][cmpt1], lb, hb)


def deplacement_bille(lb, hb, n, bloc) : 
    """
    Cette fonction est la plus longue car elle peut afficher plusieurs éléments.
    Tout d'abord elle affiche les déplacements que l'on fais pour bouger 
    la bille, ensuite lorsque la bille arrive au point d'arriver, c'est-à-dire 
    au dernier bloc, on retourne 'gagnée', on a aussi la posssibilité de pousser
    un bloc dans cette fonction.
    Puis, si l'utilisateur appuie sur 'q' (Quit), alors on quitte le jeu, s'il 
    appuie sur 'r' (Retry), alors on réessaie le niveau. Les touches 'n' (Next) 
    et 'p' (Previous) servent à aller au niveau suivant ou précedent.
    Enfin la touche 'a' (Annuler) sert à annuler les coups précedent avec l'aide 
    de plusieurs listes.
    """
    i, j, dep = 0, 0, 0
    # Enregistre le temps de départ dans une variable
    temps_depart = time.time()
    # Créer deux liste pour i et j qui commence par 0 le point de départ de la bille
    ligne_i, colonne_j = [0], [0]
    long_ligne = len(ligne_i)
    long_colonne = len(colonne_j)
    # Ajouter les deux listes plus la matrice du niveau dans une liste qui s'appele 'annule'
    bloc_copie = copy.deepcopy(bloc)
    annuler = [[ligne_i[len(ligne_i)-1],colonne_j[len(colonne_j)-1],bloc_copie]]
    while True :
        # D'abord, on  efface tout puis on affiche les textes de départ en fonction de la largeur et longueur
        efface_tout()
        affiche_texte_bis()
        largeur = (taille_x/2) - 100
        texte(largeur, 20, 'NIVEAU ' + str(jeu + 1), 'grey', taille = 30, police = 'Garamond')
        temps = affiche_time(temps_depart)
        largeur = taille_x - 240
        longueur = taille_y - 50
        texte(largeur, longueur, 'Temps = '+str(temps), 'darkred', police = 'Garamond')
        texte(10, longueur, 'Déplacement = '+str(dep), 'darkred', police = 'Garamond')
        # On affiche aussi les blocs on fonction du niveau et en fonction des déplacements de la bille
        bloc_affiche(lb, hb, n, i, j, bloc)
        evenement = donne_evenement()
        typeEv = type_evenement(evenement)
        if typeEv == 'Touche':
            nomTouche = touche(evenement)
            # La bille va vers la gauche si le joueur appuie sur la flèche gauche
            if nomTouche == 'Left' :
                # la bille ne pourra pas aller vers la gauche s'il n'y a pas de bloc de ce coté là
                if j == 0 :
                    nomTouche != 'Left'
                elif bloc[i][j - 1] > bloc[i][j] + 1 :
                    nomTouche != 'Left'
                elif bloc[i][j - 1] < (bloc[i][j] - 1) :
                    nomTouche != 'Left'
                elif bloc[i][j - 1] == bloc[i][j] + 1 :
                    if (j - 1) == 0 :
                        nomTouche != 'Left'
                    # S'il y a un bloc au même niveau que la bille alors le bloc sera poussé
                    elif bloc[i][j - 2] < bloc[i][j - 1] :
                        bloc[i][j - 2] += 1
                        bloc[i][j - 1] -= 1
                        dep += 1
                        # la bille se déplace à l'aide des coordonnées i et j
                        j -= 1
                        # Ajout de cette nouvelle valeur de j dans une liste 
                        colonne_j.append(j)
                        long_colonne = len(colonne_j) - 1
                        # Faire une copie de notre matrice du niveau pour ensuite l'ajouter dans notre liste annuler
                        bloc_copie = copy.deepcopy(bloc)
                        # Ajout de la valeur de i, j et de la matrice du niveau dans une liste à chaque déplacement
                        annuler.append([i,['colonne',colonne_j[long_colonne]],bloc_copie])
                else :
                    dep += 1
                    j -= 1
                    colonne_j.append(j)
                    long_colonne = len(colonne_j) - 1
                    bloc_copie = copy.deepcopy(bloc)
                    annuler.append([i,['colonne',colonne_j[long_colonne]],bloc_copie])
                    # La boucle s'arrête si l'utilisateur à gagné c'est-à-dire s'il arrive au dernier bloc
                    if i == (n - 1) and j == (n - 1) :
                        return ['gagné', temps, dep]

            elif nomTouche == 'Right' :
                if j == (n - 1) :
                    nomTouche != 'Right'
                elif bloc[i][j + 1] > bloc[i][j] +1 :
                    nomTouche != 'Right'
                elif bloc[i][j + 1] < (bloc[i][j] - 1) :
                    nomTouche != 'Right'
                elif bloc[i][j + 1] == bloc[i][j] + 1 :
                    if (j + 1) == (n - 1) :
                        nomTouche != 'Right'
                    elif bloc[i][j + 2] < bloc[i][j + 1] :
                        bloc[i][j + 2] += 1
                        bloc[i][j + 1] -= 1
                        dep += 1
                        j += 1
                        colonne_j.append(j)
                        long_colonne = len(colonne_j) - 1
                        bloc_copie = copy.deepcopy(bloc)
                        annuler.append([i,['colonne',colonne_j[long_colonne]],bloc_copie])
                else :
                    dep += 1
                    j += 1
                    colonne_j.append(j)
                    long_colonne = len(colonne_j) - 1
                    bloc_copie = copy.deepcopy(bloc)
                    annuler.append([i,['colonne',colonne_j[long_colonne]],bloc_copie])
                    if i == (n - 1) and j == (n - 1) :
                        return ['gagné', temps, dep]

            elif nomTouche == 'Down' :
                if i == (n - 1) :
                    nomTouche != 'Down'
                elif bloc[i + 1][j] > bloc[i][j] + 1 :
                    nomTouche != 'Down'
                elif bloc[i + 1][j] < (bloc[i][j] - 1) :
                    nomTouche != 'Down'
                elif bloc[i + 1][j] == bloc[i][j] + 1 :
                    if (i + 1) == (n - 1) :
                        nomTouche != 'Down'
                    elif bloc[i + 2][j] < bloc[i + 1][j] :
                        bloc[i + 2][j] += 1
                        bloc[i + 1][j] -= 1
                        dep += 1
                        i += 1
                        ligne_i.append(i)
                        long_ligne = len(ligne_i) - 1
                        bloc_copie = copy.deepcopy(bloc)
                        annuler.append([['ligne',ligne_i[long_ligne]],j,bloc_copie])
                else :
                    dep += 1
                    i += 1
                    ligne_i.append(i)
                    long_ligne = len(ligne_i) - 1
                    bloc_copie = copy.deepcopy(bloc)
                    annuler.append([['ligne',ligne_i[long_ligne]],j,bloc_copie])
                    if i == (n - 1) and j == (n - 1) :
                        return ['gagné', temps, dep]

            elif nomTouche == 'Up' :
                if i == 0 :
                    nomTouche != 'Up'
                elif bloc[i - 1][j] > bloc[i][j] + 1 :
                    nomTouche != 'Up'
                elif bloc[i - 1][j] < (bloc[i][j] - 1) :
                    nomTouche != 'Up'
                elif bloc[i - 1][j] == bloc[i][j] + 1 :
                    if (i - 1) == 0 :
                        nomTouche != 'Up'
                    elif bloc[i - 2][j] < bloc[i - 1][j] :
                        bloc[i - 2][j] += 1
                        bloc[i - 1][j] -= 1
                        dep += 1
                        i -= 1
                        ligne_i.append(i)
                        long_ligne = len(ligne_i) - 1
                        bloc_copie = copy.deepcopy(bloc)
                        annuler.append([['ligne',ligne_i[long_ligne]],j,bloc_copie])
                else :
                    dep += 1
                    i -= 1
                    ligne_i.append(i)
                    long_ligne = len(ligne_i) - 1
                    bloc_copie = copy.deepcopy(bloc)
                    annuler.append([['ligne',ligne_i[long_ligne]],j,bloc_copie])
                    if i == (n - 1) and j == (n - 1) :
                        return ['gagné', temps, dep]
            # La fonction retourne 'q' si l'utilisateur appuie sur 'q', de même pour les autres touches
            elif nomTouche == 'q' :
                return 'q'
            elif nomTouche == 'r' :
                return 'r'
            elif nomTouche == 'n' :
                return 'n'
            elif nomTouche == 'p' :
                return 'p'
            elif nomTouche == 'a' :
                long_ligne = len(ligne_i) - 1
                long_colonne = len(colonne_j) - 1
                # Si le dernier chiffre de la liste annuler est celui de la liste de i
                if annuler[len(annuler) - 1][0] == ['ligne',ligne_i[long_ligne]] :
                    # Supprime les dernier éléments des deux listes 
                    annuler.pop()
                    ligne_i.pop()
                    long_ligne = len(ligne_i) - 1
                # Si le dernier chiffre de la liste annuler est celui de la liste de j
                elif annuler[len(annuler) - 1][1] == ['colonne',colonne_j[long_colonne]] :
                    annuler.pop()
                    colonne_j.pop()
                    long_colonne = len(colonne_j) - 1
                # Matrice du niveau prend la copie de la valeur enregistrée dans la liste annuler
                bloc = copy.deepcopy(annuler[len(annuler) - 1][2])
                # De même pour i et j qui eux ne prennent pas de copie
                i = ligne_i[long_ligne]
                j = colonne_j[long_colonne]
        mise_a_jour()


def fct_gagner(jeu, temps_final, deplacement) :
    """
    Cette fonction prend en pramètre le compteur 'jeu', le temps que l'on a pris 
    pour finir le niveau et aussi le nombre de déplacement fais. Lorsque l'on a 
    gagné le niveau un message s'affiche avec aussi l'apparition de notre 
    meilleur score. De plus, nous pouvons recommencer, quitter, ou passer au 
    niveau suivant.
    """
    # Récupère le meilleur score du joueur
    Score_niveau, Best_liste = best_score(jeu, temps_final, score_joueur)
    # Modifie le fichier du joueur en ecrivant tous ses meilleurs score
    ecrire_score = open('../fichiers/score/' + score_joueur,'w')
    ecrire_best_score = open('../fichiers/score/Score.txt','w')
    modifier_fichier_score(Score_niveau, ecrire_score, compteur=0)
    modifier_fichier_score(Best_liste, ecrire_best_score, compteur=0)
    while True :
        efface_tout()
        rectangle(0, 0, taille_x, taille_y,  'white', 'white')
        largeur = (taille_x/3)-200
        longueur = (taille_y/2)
        # Affiche les diférents texte en fonction de la longueur et de la largeur
        texte(15, 15,'Votre Meilleur Score : '+str(Score_niveau[jeu]),'darkred', taille=22, police='Garamond')
        texte(15, 55,'Meilleur Score : ' + str(Best_liste[jeu]), 'darkblue', taille=22, police='Garamond')
        texte(taille_x/3+10, longueur-40, 'Félicitation !', 'darkblue', police='Garamond')
        texte(largeur, longueur, 'Vous avez gagné ce niveau en '+str(temps_final)+' secondes','darkblue', taille = 22, police='Garamond')
        texte(largeur+125, longueur+40, 'et avec '+str(deplacement)+' déplacements', 'darkblue', police='Garamond')
        largeur = taille_x - 150
        texte(largeur, 10, 'R : Retry\nN : Next\nQ : Quit', 'darkblue', taille=22, police = 'Garamond')
        evenement = donne_evenement()
        typeEv = type_evenement(evenement)
        if typeEv == 'Touche' :
            nomTouche = touche(evenement)
            # Si le joueur appuie sur l'une de ses touches (n, q, r), alors la fonction renvoie cette lettre
            if nomTouche == 'n' :
                return 'n'
            elif nomTouche == 'q' :
                return 'q'
            elif nomTouche == 'r' :
                return 'r'
        mise_a_jour()


def affiche_time(temps_depart) :
    """
    Cette fonction affiche le temp qui change à chaque fois dans notre fonction
    'affiche_bille()', mais le temps de départ ne change pas. Mais, on récupère
    le 'temps_après' qui change tout le temps à chaque mouvement de la bille.
    Puis la fonction 'time.gmtime()' affiche la conversion (année, mois, jour, ()
    heure, minute, secondes, jour de la semaine, jour de l'année, heure local).
    Cette fonction renvoie le temps en secondes plus le reste du temps qui a été 
    arrondis qui sont les microsecondes.
    """
    # Récupère le temps après le temps de départ que nous avons en paramètre
    temps_apres = time.time() - temps_depart
    # Recupère la date d'aujourd'hui avec l'heure dans un tuple à l'aide de la fonction time.gmtime()
    time_liste = time.gmtime(temps_apres)
    # On prend le reste du temps qui seront les microsecondes
    microseconde = temps_apres - time_liste[5]
    # Arrondit ce chiffre au dixième près
    arrondi_ms = round(microseconde, 1)
    # Temps de fin qui est la somme des secondes et des microsecondes
    temps = time_liste[5] + arrondi_ms
    # Renvoie le temps 
    return temps


def liste_fichier_score(fichier_score, Score_niveau=[]) :
    """
    C'est une fonction récursive qui crée la liste des temps fais par le joueur
    précédemment qui a été dans un fichier. Cette fonction est possible seulement
    s'il exsite dèjà un fichier à son nom.
    """
    chiffre_final, cmpt = '0', 0
    # Lit le fichier ligne par ligne
    total = fichier_score.readline()
    # Si la dernière ligne est juste un saut de ligne alors la liste est fini
    if total == '\n' :
        # On renvoie donc la liste de fin
        return Score_niveau
    # Le chiffre_final est égale à l'élément contenu dans le fichier sans le saut de ligne
    while cmpt < len(total) - 1 :
        chiffre_final += total[cmpt]
        cmpt += 1
    # Ajout de ce chiffre à virgule dans la liste 
    Score_niveau.append(float(chiffre_final))
    # Renvoie la fonction pour qu'elle lise la prochaine ligne du fichier
    return liste_fichier_score(fichier_score, Score_niveau)


def best_score(jeu, temps_final, score_joueur) :
    """
    La fonction best_score modifie la liste crée par la fonction 
    'liste_fichier_score' pour afficher tout les meilleurs temps du joueur.
    """
    # Ouverture du fichier qui contient tout les score du joueur
    fichier_score = open('../fichiers/score/' + score_joueur,'r')
    fichier_best_score = open('../fichiers/score/Score.txt','r')
    # Affiche la liste des différents score fais par le joueur
    Score_niveau = liste_fichier_score(fichier_score, Score_niveau=[])
    Best_liste = liste_fichier_score(fichier_best_score, Score_niveau=[])
    # Si le temps fais par le joueur est plus petit que son ancien temps 
    if temps_final < Score_niveau[jeu] :
        # La liste sera modifier par le temps final qu'il a fais
        Score_niveau[jeu] = temps_final
    if Score_niveau[jeu] < Best_liste[jeu] :
        Best_liste[jeu] = Score_niveau[jeu]
    # Renvoie la liste après les modifications
    return Score_niveau,Best_liste


def modifier_fichier_score(Score_niveau, ecrire_score, compteur=0) :
    """
    Cette fonction modifie le fichier de départ en écrivant le contenu de la 
    liste 'Score_niveau' dans ce fichier. c'est une fonction récursive qui 
    s'arrête lorsque le compteur arrive au dernier nombre de la liste.
    """
    # Si le compteur est égale à la longueur de la liste 
    if compteur == len(Score_niveau) :
        # Ajout d'un saut de ligne à la fin du fichier
        ecrire_score.writelines('\n')
        # Ferme le fichier
        ecrire_score.close()
        # La fonction s'arrête à ce moment-là
        return None
    # Ajout d'un contenu en str + un saut de ligne avec la fonction writelines
    ecrire_score.writelines(str(Score_niveau[compteur]) + '\n')
    # Renvoie la fonction de façon récursive
    return modifier_fichier_score(Score_niveau, ecrire_score, compteur + 1)


def nom_joueur() :
    """
    Cette fonction demande le nom du joueur au début du jeu puis renvoie le nom
    du fichier contenant les scores du joueur s'il existe, sinon il crée un 
    fichier qui aura comme meilleur score '1000.0' à chaque niveau.
    """
    # Demande le nom du joueur 
    nom = input('Nom du joueur ? ')
    # Chemin contenant tout les fichiers score
    chemin = "../fichiers/score/"
    # Fait une liste des fichiers présent dans le répertoire
    fichiers_nom = os.listdir(chemin)
    fichiers_nom.sort() # Range la liste
    # Si le fichier avec le nom existe alors on renvoie le nom du fichier
    if nom + '.txt' in fichiers_nom :
        return nom + '.txt'
    # Sinon on crée un fichier (txt) avec ce nom 
    else :
        # Le mode 'a' est pour ajouter du contenu dans le fichier
        score_joueur = open(chemin + nom + '.txt', 'a')
        cmpt = 0
        # Tant que le compteur est inférieur à la longeur de la liste des niveaux
        while cmpt < len(fichiers) + 1 :
            if cmpt < len(fichiers) :
                score_joueur.write('1000.0\n')
            elif cmpt == len(fichiers) :
                # Ajout d'un saut de ligne à la fin du fichier
                score_joueur.write('\n')
            cmpt += 1
        # Renvoie le nom du fichier.txt
        return nom + '.txt'


def recommencer_ou_arret_jeu() :
    """
    Cette fonction affiche un message pour savoir si le joueur veut 
    recommencer le jeu ou s'il veut quitter. Ainsi, il doit appuyer sur l'une
    des touches pour soit recommencer le jeu avec 'j', soit recommencer le 
    niveau précédent avec 'p' ou sinon quitter le jeu ave 'q'.
    """
    while True :
        efface_tout()
        rectangle(0, 0, taille_x, taille_y,  'white', 'white')
        longueur = (taille_y/2) - 40
        largeur = (taille_x/3)
        texte(largeur, longueur, '       THE END !\n Le jeu est terminé', 'darkblue', taille=22, police = 'Garamond')
        texte(taille_x-300, 10, 'J : Retry the Game\n   P : Previous\n      Q : Quit', 'darkblue', taille=22, police = 'Garamond')
        texte(200,(taille_y)-50, 'Cliquer pour afficher vos scores !','darkblue',taille=22, police='Garamond')
        evenement = donne_evenement()
        typeEv = type_evenement(evenement)
        if typeEv == 'Touche':
            nomTouche = touche(evenement)
            # Si le joueur appuie sur l'une des touches ci-dessous alors la fonction renvoie la lettre 
            if nomTouche == 'j' :
                return 'j'
            elif nomTouche == 'p' :
                return 'p'
            elif nomTouche == 'q' :
                return 'q'
        elif typeEv == 'ClicGauche' :
            return 'clic'
        mise_a_jour()


def affiche_score_fin(joueur_score) :
    """
    Cette fonction affiche un tableau à la fin du jeu qui indique tout les scores
    du joueur, tout les meilleurs scores qu'il a pus faire et aussi tout les 
    meilleurs score de tout les joueurs en intégrale.
    """
    efface_tout()
    # Affiche le fond en blanc avec une image
    rectangle(0, 0, taille_x, taille_y,  'white', 'white')
    # Affiche les chiffres à l'aide des fichiers enregistrés qui contient les meilleurs scores
    fichier_score = open('../fichiers/score/' + score_joueur,'r')
    fichier_best_score = open('../fichiers/score/Score.txt','r')
    Score_niveau = liste_fichier_score(fichier_score, Score_niveau=[])
    Best_liste = liste_fichier_score(fichier_best_score, Score_niveau=[])
    longeur = taille_x/4
    largeur = taille_y-20
    # Dessine des lignes pour une apparition de tableau
    ligne((taille_x/4),0,(taille_x/4),taille_y-50,epaisseur=3)
    ligne((taille_x/2),0,(taille_x/2),taille_y-50,epaisseur=3)
    ligne((taille_x-(taille_x/4)),0,(taille_x-(taille_x/4)),taille_y-50,epaisseur=3)
    
    texte(longeur+50,(taille_y)-50, ' Cliquer pour quitter !','darkblue',taille=22, police='Garamond')
    # Affichage des textes à chaque début de colonne
    texte(50,20,' Niveau',taille=18,police='Garamond')
    texte(longeur+20,20,'   Vos Scores', taille=18, police='Garamond')
    texte((2*longeur)+20,20,'       Vos \nmeilleurs Score',taille=18,police='Garamond')
    texte((taille_x-longeur)+20,20,'      Tout les\nmeilleurs Scores',taille=18,police='Garamond')
    # Affihce tout les nombres de chaque liste
    distance = 0
    for compteur in range(len(joueur_score)) :
        texte(100,((taille_y/9)+30) + distance,str(compteur+1),taille=18,police='Garamond')
        texte(longeur+20,((taille_y/9)+30) + distance,str(joueur_score[compteur]),taille=18,police='Garamond')
        texte((2*longeur)+20,((taille_y/9)+30) + distance,str(Score_niveau[compteur]),taille=18,police='Garamond')
        texte((taille_x-longeur)+20,((taille_y/9)+30) + distance,str(Best_liste[compteur]),taille=18,police='Garamond')
        # Augmente la distance pour chaque ligne du tableau
        distance += 60



if __name__ == "__main__":
    # Chemin pour accéder aux fichiers qui contient les niveaux
    chemin = "../fichiers/maps/"
    # La fonction "os.listdir" prend un nom de chemin en paramètre et renvoie une liste les fichers que contient le répertoire
    fichiers = os.listdir(chemin)
    # La methode "sort()" range la liste dans l'ordre
    fichiers.sort()
    score_joueur = nom_joueur()
    taille_x = 900
    taille_y = 900
    # Crée une fenêtre avec la fonction ci-dessous à l'aide des coordonnées x et y ci-dessus
    cree_fenetre(taille_x, taille_y)
    affiche_texte()
    # Affihce le niveau en fonction de la difficulté donné
    if menu() == 'facile':
        jeu = 0
        joueur_score = []
    elif menu() == 'moyen':
        jeu = 3
        # Ajout de 'None' dans la liste car les niveaux précédent n'ont pas été joué
        joueur_score = ['None','None','None']
    elif menu() == 'difficile' :
        jeu = 6
        joueur_score = ['None','None','None','None','None','None']
    
    # La boucle while commence avec un compteur 'jeu' qui doit être inférieur ou égale à la taille de la liste
    while jeu <= (len(fichiers)) :
        # Ouvre et lis le fichier
        niveau = open(chemin + fichiers[jeu],'r')
        bloc, hauteurmax = liste_affiche(niveau, Bloc = [], hauteurmax = 0)
        n = len(bloc[0])
        # Coordonnées de lb et hb en fonction de la taille de la grille
        lb = ((taille_x // 2) - 30) / (len(bloc))
        hb = min(1.5*lb, ((taille_y//2) - 70)/(hauteurmax + 1))
        bloc_affiche(lb, hb, n, 0, 0, bloc)
        resultat = deplacement_bille(lb, hb, n, bloc)
        # Si la fonction "deplacement_bille" renvoie 'r' alors on rééssaie le niveau, donc le compteur reprend la même valeur
        if resultat == 'r' :
            jeu -= 1
            # Supprime le dernier score enregistré
            joueur_score.pop()

        # Si cette fonction renvoie 'q' alors on quitte le jeu
        elif resultat == 'q' :
            break

        # Si cette même fonction renvoie 'gagné' alors un message est affiché, puis on attend un clique pour passer au niveau suivant
        elif resultat[0] == 'gagné' :
            # Ajout des scores que le joueur fais dans une liste
            joueur_score.append(resultat[1])
            win = fct_gagner(jeu, resultat[1], resultat[2])
            if win == 'r' :
                jeu -= 1
                joueur_score.pop()
            elif win == 'q' :
                break

        # Le renvoie de la touche 'n' est pour changer de niveau donc on a juste à passer
        elif resultat == 'n' :
            joueur_score.append('None')
            pass

        # Puis, le renvoie de la touche 'p' est pour aller au niveau précédemment
        elif resultat == 'p' :
            # Si le niveau est de 0 alors il n'y a pas de niveau précédent
            if jeu == 0 :
                jeu -= 1
            # Pour les autres niveau le compteur 'jeu' prend la valeur du niveau précédent
            else :
                jeu -= 2
            joueur_score.pop()
        jeu += 1
        if jeu == (len(fichiers)) :
            fin = recommencer_ou_arret_jeu()
            # Si la fonction ci-dessus renvoie 'j' alors on recommence le jeu, donc le jeu prend la valeur de 0
            if fin == 'j' :
                # Le compteur jeu reprend la valeur 0 pour recommencer le jeu
                jeu = 0
            elif fin == 'p' :
                # Pour revenir au niveau précédent, on enlève un au compteur
                jeu -= 1
            elif fin == 'q' :
                # On sort de la boucle pour quitter le jeu
                break
            elif fin == 'clic' :
                # Affiche le tableau des scores avec la fonction ci-dessous
                affiche_score_fin(joueur_score)
                attente_clic()
                break

    # Une fois la boucle fini, on ferme la fenêtre
    ferme_fenetre()


